from django.contrib import admin
from api.models.protocols import Protocol, ProtocolDataSource, \
    Organization, ProtocolUser, ProtocolUserCredentials, DataSource, \
    ProtocolDataSourceLink


from django.contrib import admin


class OrganizationAdmin(admin.ModelAdmin):
    list_filter = ['name']
    search_fields = ['name']
    list_display = ['name', 'subject_id_label']

admin.site.register(Organization, OrganizationAdmin)


class DataSourceAdmin(admin.ModelAdmin):
    list_filter = ['created', 'modified']
    search_fields = ['name']
    list_display = ['name', 'description']

admin.site.register(DataSource, DataSourceAdmin)


class ProtocolUserCredentialsAdmin(admin.ModelAdmin):
    list_filter = ['protocol', 'user', 'data_source', 'created', 'modified']
    search_fields = ['user__username']
    list_display = ['protocol', 'data_source', 'user']
    raw_id_fields = ("data_source", "user")

admin.site.register(ProtocolUserCredentials, ProtocolUserCredentialsAdmin)


class ProtocolAdmin(admin.ModelAdmin):
    list_filter = ['name', 'created', 'modified']
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Protocol, ProtocolAdmin)


class ProtocolDataSourceAdmin(admin.ModelAdmin):
    list_filter = ['protocol', 'data_source', 'path', 'created', 'modified']
    list_display = ['protocol', 'data_source', 'path']
    search_fields = ['protocol__name', 'data_source__name', 'path']

admin.site.register(ProtocolDataSource, ProtocolDataSourceAdmin)


class ProtocolUserAdmin(admin.ModelAdmin):
    list_filter = ['user', 'protocol', 'created', 'modified']
    list_display = ['user', 'protocol']
    search_fields = ['user__username', 'protocol__name']

admin.site.register(ProtocolUser, ProtocolUserAdmin)


class ProtocolDataSourceLinkAdmin(admin.ModelAdmin):
    list_display = ['pds_one', 'pds_two']

admin.site.register(ProtocolDataSourceLink, ProtocolDataSourceLinkAdmin)
