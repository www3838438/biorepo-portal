import json
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.core.cache import cache

from ehb_client.requests.exceptions import PageNotFound
from ehb_client.requests.subject_request_handler import Subject
from ehb_client.requests.external_record_request_handler import ExternalRecord

from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from .serializers import UserSerializer, GroupSerializer, OrganizationSerializer,\
    DataSourceSerializer, ProtocolSerializer, ProtocolDataSourceSerializer,\
    eHBSubjectSerializer
from .models.protocols import Organization, Protocol, DataSource, ProtocolDataSource,\
    ProtocolUserCredentials
from .ehb_service_client import ServiceClient
from .utilities import SubjectUtils

from copy import deepcopy


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

    def getExternalRecords(self, pds, subject):
        # TODO: Need to cache this heavily!
        er_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD)
        er_label_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD_LABEL)
        lbls = er_label_rh.query()
        try:
            pds_records = er_rh.get(
                external_system_url=pds.data_source.url, path=pds.path, subject_id=subject['id'])
        except PageNotFound:
            pds_records = []

        r = []
        for ex_rec in pds_records:
            # Convert ehb-client object to JSON and then parse as py dict
            e = json.loads(ex_rec.json_from_identity(ex_rec))
            # Map label descriptions from the eHB to External Records
            for label in lbls:
                if e['label'] == label['id']:
                    if label['label'] == '':
                        e['label_desc'] = 'Record'
                    else:
                        e['label_desc'] = label['label']
            e['pds'] = pds.id
            r.append(e)

        return r

    @detail_route(methods=['post'])
    def add_subject(self, request, *args, **kwargs):
        """
        Add a subject to the protocol

        Expects a request body of the form:
        {
            "first_name": "John",
            "last_name": "Doe",
            "organization_subject_id": "123123123",
            "organization": "1",
            "dob": "2000-01-01"
        }
        """
        protocol = self.get_object()
        subject = json.loads(request.body)

        new_subject = Subject(
            first_name=subject['first_name'],
            last_name=subject['last_name'],
            organization_id=int(subject['organization']),
            organization_subject_id=subject['organization_subject_id'],
            dob=datetime.strptime(subject['dob'], '%Y-%m-%d')
        )
        srh = ServiceClient.get_rh_for(record_type=ServiceClient.SUBJECT)
        org = Organization.objects.get(pk=new_subject.organization_id)
        errors = []
        try:
            subject = srh.get(
                organization_id=new_subject.organization_id,
                organization_subject_id=new_subject.organization_subject_id)
            success = True
            # If found this indicates the subject is already in the ehb for
            # this organization, but not necessarily for this protocol.
            # That will be checked below in the external record search
            prefix = "A subject with this " + org.subject_id_label + " exists but with "
            if subject.first_name != new_subject.first_name:
                success = False
                errors.append(prefix + "first name: " + subject.first_name)
            if subject.last_name != new_subject.last_name:
                success = False
                errors.append(prefix + "last name: " + subject.last_name)
            if subject.dob != new_subject.dob.date():
                success = False
                errors.append(prefix + "birth date: " + str(subject.dob))
        except PageNotFound:
            # Subject is not in the system so create it
            r = srh.create(new_subject)[0]
            success = r.get('success')
            errors = r.get('errors')
            subject = r.get(Subject.identityLabel)

        # Dont proceed if creation was not a success
        if not success:
            subject = json.loads(Subject.json_from_identity(subject))
            return Response([success, subject, errors], status=422)

        if not errors:
            errors = []
        # First check if the subject is already in the group.
        if protocol.getSubjects() and subject in protocol.getSubjects():
            # Subject is already in protocol
            errors.append(
                'This subject ' + org.subject_id_label +
                ' has already been added to this project.'
            )
            logger.error("Could not add subject. They already exist on this protocol.")
            success = False
        else:
            # Add this subject to the protocol and create external record group
            if SubjectUtils.create_protocol_subject_record_group(protocol, new_subject):
                if protocol.addSubject(subject):
                    success = True
                else:
                    # Could not add subject to project
                    errors.append(
                        'Failed to complete eHB transactions. Could not add subject to project. Please try again.')
                    success = False
            else:
                # For some reason we couldn't get the eHB to add the subject to the protocol group
                errors.append(
                    'Failed to complete eHB transactions. Could not add subject to project. Please try again.')
                success = False

        subject = json.loads(Subject.json_from_identity(subject))

        # Add subject to cache
        cache_key = 'protocol{0}_sub_data'.format(protocol.id)
        cache_data = cache.get(cache_key)
        if cache_data:
            subject['external_ids'] = []
            subject['external_records'] = []
            subject['organization_name'] = org.name
            subjects = json.loads(cache_data)
            subjects.append(subject)
            cache.set(cache_key, json.dumps(subjects))
            cache.expire(cache_key, 24 * 24 * 60)
        return Response(
            [success, subject, errors],
            headers={'Access-Control-Allow-Origin': '*'},
            status=200
        )

    @detail_route(methods=['put'])
    def update_subject(self, request, *args, **kwargs):
        subject = json.loads(request.body)
        # See if subject exists
        s_rh = ServiceClient.get_rh_for(record_type=ServiceClient.SUBJECT)
        o_rh = ServiceClient.get_rh_for(record_type=ServiceClient.ORGANIZATION)
        try:
            ehb_sub = s_rh.get(id=subject['id'])
            org = Organization.objects.get(id=subject['organization_id'])
        except:
            return Response("", status=404)
        ehb_org = org.getEhbServiceInstance()
        ehb_sub.old_subject = deepcopy(ehb_sub)
        ehb_sub.first_name = subject['first_name']
        ehb_sub.last_name = subject['last_name']
        ehb_sub.organization_subject_id = subject['organization_subject_id']
        ehb_sub.organization_id = ehb_org.id
        ehb_sub.dob = datetime.strptime(subject['dob'], '%Y-%m-%d')
        update = s_rh.update(ehb_sub)[0]
        if update['errors']:
            return Response(json.dumps({'error': 'Unable to update subject'}), status=400)
        sub = json.loads(Subject.json_from_identity(update['subject']))
        sub['organization_name'] = org.name
        return Response(
            sub,
            headers={'Access-Control-Allow-Origin': '*'}
        )

    @detail_route(methods=['get'])
    def get_subject(self, request, pk, subject, *args, **kwargs):
        """
        Return a single requested subject
        """
        p = self.get_object()
        if p.isUserAuthorized(request.user):
            protocoldatasources = p.getProtocolDataSources()
            manageExternalIDs = False
            for pds in protocoldatasources:
                if pds.driver == 3:
                    ExIdSource = pds
                    manageExternalIDs = True
            s_rh = ServiceClient.get_rh_for(record_type=ServiceClient.SUBJECT)
            o_rh = ServiceClient.get_rh_for(record_type=ServiceClient.ORGANIZATION)
            try:
                subject = s_rh.get(id=subject)
                organization = o_rh.get(id=subject.organization_id)
            except:
                return Response("", status=404)
            sub = json.loads(Subject.json_from_identity(subject))
            sub['organization_name'] = organization.name
            sub['external_records'] = []
            for pds in protocoldatasources:
                sub['external_records'].extend(self.getExternalRecords(pds, sub))
            if manageExternalIDs:
                # Break out external ids into a separate object for ease of use
                sub['external_ids'] = []
                for record in sub['external_records']:
                    if record['external_system'] == 3:
                        sub['external_ids'].append(record)
            return Response(sub)
        else:
            return Response(
                {"detail": "You are not authorized to view subjects in this protocol"},
                status=403
            )

    @list_route()
    def organizations(self, request, *args, **kwargs):
        """
        Provide a list of organizations associated with a protocol
        """
        p = self.get_object()
        if p.isUserAuthorized(request.user):
            q = p.organizations.all()
            orgs = [OrganizationSerializer(org).data for org in q]
        return Response(
            orgs,
            headers={'Access-Control-Allow-Origin': '*'}
        )

    @list_route()
    def subjects(self, request, *args, **kwargs):
        """
        Returns a list of subjects associated with a protocol.
        """
        p = self.get_object()
        # Check cache
        cache_data = cache.get('protocol{0}_sub_data'.format(p.id))
        if cache_data:
            return Response(
                json.loads(cache_data),
                headers={'Access-Control-Allow-Origin': '*'}
            )
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
            # Check if the protocol has external IDs configured. If so retrieve them
            manageExternalIDs = False

            protocoldatasources = p.getProtocolDataSources()

            for pds in protocoldatasources:
                if pds.driver == 3:
                    ExIdSource = pds
                    manageExternalIDs = True

            if manageExternalIDs:
                try:
                    config = json.loads(ExIdSource.driver_configuration)
                    if 'sort_on' in config.keys():
                        # er_label_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD_LABEL)
                        # lbl = er_label_rh.get(id=config['sort_on'])
                        lbl = ''
                        addl_id_column = lbl
                except:
                    pass

            for sub in subs:
                sub['external_records'] = []
                sub['external_ids'] = []
                for pds in protocoldatasources:
                    sub['external_records'].extend(self.getExternalRecords(pds, sub))
                if manageExternalIDs:
                    # Break out external ids into a separate object for ease of use
                    for record in sub['external_records']:
                        if record['external_system'] == 3:
                            sub['external_ids'].append(record)
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
            if pds.driver_configuration != '':
                dc = json.loads(pds.driver_configuration)
            else:
                dc = {}
            # If labels are defined get label names from eHB.
            # (label_id, label_description)
            if 'labels' in dc.keys():
                er_label_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD_LABEL)
                lbls = er_label_rh.query()
                nl = []
                for l in dc['labels']:
                    for label in lbls:
                        if l == label['id']:
                            if label['label'] == '':
                                nl.append((label['id'], 'Record'))
                            else:
                                nl.append((label['id'], label['label']))
                dc['labels'] = nl
            else:
                dc['labels'] = [(1, 'Record')]

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

    @list_route()
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
                                    sub["external_records"].append(rec.json_from_identity(rec))

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
            try:
                ProtocolUserCredentials.objects.get(
                    protocol=p.protocol, data_source=p, user=request.user)
            except ProtocolUserCredentials.DoesNotExist:
                return Response([], status=403)

            res = ServiceClient.ext_rec_client.query({
                "subject_id": kwargs['subject'],
                "external_system_id": p.data_source.ehb_service_es_id,
                "path": p.path
            })[0]

            if res["success"]:
                for ex_rec in res["external_record"]:
                    t = json.loads(ex_rec.json_from_identity(ex_rec))
                    ex_recs.append(t)

        return Response(sorted(
            ex_recs, key=lambda ex_recs: ex_recs["created"]))


    @detail_route(methods=['get'])
    def available_links(self, request, *args, **kwargs):
        '''Return available links that can be made using this protocol data source
        '''
        pds = self.get_object()
        if pds.protocol.isUserAuthorized(request.user):
            res = ServiceClient.ext_rec_rel_client.get()
            if pds.driver_configuration != '':
                dc = json.loads(pds.driver_configuration)
            else:
                return Response([])
            links = []
            if not res:
                return Response([])
            for link in res:
                if 'links' in dc.keys() and link['id'] in dc['links']:
                    links.append(link)
            return Response(links)

    @detail_route(methods=['get'])
    def get_subject_record(self, request, *args, **kwargs):
        # TODO Add external id get here.
        pds = self.get_object()
        if pds.protocol.isUserAuthorized(request.user):
            res = ServiceClient.ext_rec_client.get(id=kwargs['record_id'])
            d = json.loads(res.json_from_identity(res))
            return Response(d)
        else:
            return Response(
                {"detail": "You are not authorized to view records from this protocol"},
                status=403
            )

    @detail_route(methods=['get'])
    def get_subject_record_links(self, request, *args, **kwargs):
        '''Return a list of record links for a specific record on a protocol data source
        '''
        pds = self.get_object()
        if pds.protocol.isUserAuthorized(request.user):
            res = ServiceClient.ext_rec_client.get(id=kwargs['record_id'], links=True)
            return Response(res)
        else:
            return Response(
                {"detail": "You are not authorized to view record links from this protocol"},
                status=403
            )

    @detail_route(methods=['post'])
    def create_subject_record_link(self, request, *args, **kwargs):
        '''Create a link between two subject records in the eHB
        '''
        pds = self.get_object()
        if pds.protocol.isUserAuthorized(request.user):
            data = json.loads(request.body)
            primary_rec = data['primaryRecord']
            secondary_rec = data['secondaryRecord']
            link_type = data['linkType']
            # Serialize
            primary_rec = ExternalRecord.identity_from_json(json.dumps(primary_rec))
            secondary_rec = ExternalRecord.identity_from_json(json.dumps(secondary_rec))
            res = ServiceClient.ext_rec_client.link(primary_rec, secondary_rec, link_type)
            if res['success']:
                return Response(res)
            else:
                return Response({'success': False, 'error': res['error']}, status=422)
            return Response({'success': False, 'error': 'Unknown Error'}, status=422)

    @detail_route(methods=['delete'])
    def delete_subject_record_link(self, request, *args, **kwargs):
        '''Create a link between two subject records in the eHB
        '''
        pds = self.get_object()
        if pds.protocol.isUserAuthorized(request.user):
            data = json.loads(request.body)
            primary_rec = data['primaryRecord']
            link_id = data['linkId']
            # Serialize
            primary_rec = ExternalRecord.identity_from_json(json.dumps(primary_rec))
            res = ServiceClient.ext_rec_client.unlink(primary_rec, link_id)
            if res['success']:
                return Response(res)
            return Response({'success': False }, status=422)

    @detail_route(methods=['put'])
    def update_subject_record(self, request, *args, **kwargs):
        '''
        Updates the subject record. Currently only changing the records label is
        supported.

        If successful the updated external record is returned
        '''
        pds = self.get_object()
        if pds.protocol.isUserAuthorized(request.user):
            ex_rec = json.loads(request.body)
            rec = ServiceClient.ext_rec_client.get(id=ex_rec['id'])
            rec.label_id = ex_rec['label_id']
            rec.modified = datetime.now()
            res = ServiceClient.ext_rec_client.update(rec)[0]
            if res['success']:
                ex_rec = res['external_record']
                return Response(json.loads(ex_rec.json_from_identity(ex_rec)))
            else:
                return Response({
                    'success': res['success'],
                    'errors': res['errors']},
                    status=422)
        else:
            return Response(
                {"detail": "You are not authorized to view records from this protocol"},
                status=403
            )