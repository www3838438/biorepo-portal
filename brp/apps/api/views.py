import json

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from api.serializers import UserSerializer, GroupSerializer, OrganizationSerializer,\
    DataSourceSerializer, ProtocolSerializer, ProtocolDataSourceSerializer,\
    eHBSubjectSerializer, eHBExternalRecordSerializer

from portal.models.protocols import Organization, Protocol, DataSource, ProtocolDataSource,\
    ProtocolUserCredentials
from portal.ehb_service_client import ServiceClient


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class DataSourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows data sources to be viewed or edited
    """
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows organizations to be viewed or edited
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class ProtocolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows protocols to be viewed.
    """
    queryset = Protocol.objects.all()
    serializer_class = ProtocolSerializer

    def list(self, request, *args, **kwargs):
        protocols = []

        for p in Protocol.objects.all():
            if request.user in p.users.all():
                protocols.append(ProtocolSerializer(p, context={'request': request}).data)

        return Response(protocols)

    @list_route()
    def subjects(self, request, *args, **kwargs):
        """
        Returns a list of subjects associated with a protocol.
        """
        p = self.get_object()

        if p.isUserAuthorized(request.user):
            subjects = p.getSubjects()
            organizations = p.organizations.all()
            if subjects:
                subs = [eHBSubjectSerializer(sub).data for sub in subjects]
            else:
                return Response([])
            ehb_orgs = []
            # We can't rely on Ids being consistent across apps so we must
            # append the name here for display downstream.
            for o in organizations:
                ehb_orgs.append(o.getEhbServiceInstance())
            for sub in subs:
                for ehb_org in ehb_orgs:
                    if sub['organization_id'] == ehb_org.id:
                        sub['organization_name'] = ehb_org.name
        else:
            return Response(
                {"detail": "You are not authorized to view subjects in this protocol"},
                status=403
            )

        if subjects:
            return Response(
                subs,
                headers={'Access-Control-Allow-Origin': '*'}
            )

        return Response([])

    @list_route()
    def data_sources(self, request, *args, **kwargs):
        """
        Returns a list of protocol datasources associated with this protocol

        Also determines authorization for each protocol datasource based on
        the user making the request.
        """
        p = self.get_object()

        ds = []

        for pds in p.getProtocolDataSources():
            t = ProtocolDataSourceSerializer(pds, context={'request': request}).data
            # Parse ProtocolDataSource configuration
            dc = json.loads(pds.driver_configuration)
            t["driver_configuration"] = dc
            # Determine Authorization
            try:
                ProtocolUserCredentials.objects.get(
                    protocol=p, data_source=pds, user=request.user)
                t["authorized"] = True
            except ProtocolUserCredentials.DoesNotExist:
                t["authorized"] = False
            # Include DataSource details
            t["data_source"] = DataSourceSerializer(pds.data_source).data

            ds.append(t)

        return Response(sorted(
            ds, key=lambda ds: ds["display_label"]))


class ProtocolDataSourceViewSet(viewsets.ModelViewSet):
    queryset = ProtocolDataSource.objects.all()
    serializer_class = ProtocolDataSourceSerializer

    def buildQueryParams(self, subjects, es_id, path):
        params = []
        for subject in subjects:
            params.append({
                "subject_id": subject.id,
                "external_system_id": es_id,
                "path": path
            })
        return params

    def subjects(self, request, *args, **kwargs):
            """
            Returns a list of subjects associated with the protocol datasource and their
            """
            p = self.get_object()
            subjects = p.protocol.getSubjects()
            organizations = p.protocol.organizations.all()
            if p.protocol.isUserAuthorized(request.user):
                if subjects:
                    params = self.buildQueryParams(subjects, p.data_source.ehb_service_es_id, p.path)
                    res = ServiceClient.ext_rec_client.query(*params)
                    subjects = [eHBSubjectSerializer(subject).data for subject in subjects]

                    ehb_orgs = []
                    # We can't rely on Ids being consistent across apps so we must
                    # append the name here for display downstream.
                    for o in organizations:
                        ehb_orgs.append(o.getEhbServiceInstance())
                    for sub in subjects:
                        sub.update({"external_records": []})
                        for ehb_org in ehb_orgs:
                            if sub['organization_id'] == ehb_org.id:
                                sub['organization_name'] = ehb_org.name
                    for ex_rec in res:
                        if ex_rec["success"]:
                            for sub in subjects:
                                for rec in ex_rec["external_record"]:
                                    if rec.subject_id == sub["id"]:
                                        sub["external_records"].append(eHBExternalRecordSerializer(rec).data)

                    return Response({
                        "subjects": subjects,
                        "count": len(subjects)
                        })
                else:
                    return Response({
                        "subjects": [],
                        "count": 0
                    })
            else:
                return Response(
                    {"detail": "You are not authorized to view subjects from this protocol datasource"},
                    status=403
                )

    @list_route()
    def subject_records(self, request, *args, **kwargs):
        """
        Returns a list of records associated with a specific subject on a protocol data source.
        """
        p = self.get_object()
        ex_recs = []
        if p.protocol.isUserAuthorized(request.user):
            res = ServiceClient.ext_rec_client.query({
                "subject_id": kwargs['subject'],
                "external_system_id": p.data_source.ehb_service_es_id
            })[0]
            if res["success"]:
                for ex_rec in res["external_record"]:
                    t = eHBExternalRecordSerializer(ex_rec).data
                    t['label'] = ServiceClient.ext_rec_label_client.get(id=t['label_id'])['label']

                    ex_recs.append(t)

        return Response(ex_recs)
