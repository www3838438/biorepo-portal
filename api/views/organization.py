from rest_framework import viewsets
from api.models.protocols import Organization
from api.serializers import OrganizationSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows organizations to be viewed or edited
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
