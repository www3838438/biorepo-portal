from rest_framework import viewsets
from api.serializers import DataSourceSerializer
from api.models.protocols import DataSource


class DataSourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows data sources to be viewed or edited
    """
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
