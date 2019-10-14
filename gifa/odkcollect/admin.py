from django.contrib import admin

from odkcollect.models import ODKConnector
from odkcollect.forms import ODKConnectorAdminForm

class ODKConnectorsAdmin(admin.ModelAdmin):
    form = ODKConnectorAdminForm
    ordering = ['-con_id']
    list_display = [
        'con_id',
        'con_nama',
        'db_name',
        'db_username',
        'geometry_type',
        'publish'
    ]
    list_display_links = (
        'con_id',
        'con_nama',
        'db_name',
        'db_username',
        'geometry_type',
        'publish'
    )
    list_filter = [
        'con_nama',
        'con_id'
    ]
    search_fields = ['con_nama', 'db_name', 'db_username', 'odk_table_name']

admin.site.register(ODKConnector, ODKConnectorsAdmin)
