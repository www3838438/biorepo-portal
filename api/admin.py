from django.contrib import admin
from api.models.protocols import Protocol, ProtocolDataSource, \
    Organization, ProtocolUser, ProtocolUserCredentials

admin.site.register([
    Protocol, ProtocolDataSource, Organization, ProtocolUser,
    ProtocolUserCredentials])
