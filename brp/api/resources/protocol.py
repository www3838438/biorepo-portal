from django.conf.urls import patterns, url
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import serializers, viewsets, routers

from portal.models.protocols import Protocol
from api.resources.ehb.subject import eHBSubjectSerializer


class ProtocolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Protocol
        fields = ('name', 'users', 'organizations', 'data_sources', 'id')


class ProtocolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows protocols to be viewed.
    """
    queryset = Protocol.objects.all()
    serializer_class = ProtocolSerializer

    def list(self, request, *args, **kwargs):
        protocols = []

        for p in Protocol.objects.all():
            if p.users.all().__contains__(request.user):
                protocols.append(ProtocolSerializer(p, context={'request': request}).data)

        return Response(protocols)

    @list_route()
    def subjects(self, request, *args, **kwargs):
        """
        Returns a list of subjects associated with a protocol.
        """
        p = self.get_object()
        print args
        if p.isUserAuthorized(request.user):
            subjects = p.getSubjects()
        else:
            return Response(
                {"detail": "You are not authorized to view subjects in this protocol"},
                status=403
            )

        if subjects:
            return Response([eHBSubjectSerializer(sub).data for sub in subjects])

        return Response([])


router = routers.DefaultRouter()
router.register(r'protocols', ProtocolViewSet)

# Resource endpoints
urlpatterns = patterns(
    '',
    url(r'^$', ProtocolViewSet, name='protocol'),)
