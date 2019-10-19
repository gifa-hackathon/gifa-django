from django.contrib import admin

from mapservice.models import MapServices, LayerServices


class LayerServicesAdmin(admin.ModelAdmin):
    ordering = ['-layer_name']
    list_display = [
        'layer_name',
        'map_services',
        'layer_display_name',
    ]
    list_display_links = (
        'layer_name',
        'map_services',
        'layer_display_name',
    )
    list_filter = [
        'layer_name',
    ]
    search_fields = ['layer_name', 'map_services', 'layer_display_name']


class MapServicesAdmin(admin.ModelAdmin):
    ordering = ['-service_id']
    list_display = [
        'service_id',
        'service_name',
        'description',
        'service_attribution',
        'service_url',
        'publish'
    ]
    list_display_links = (
        'service_id',
        'service_name',
        'description',
        'service_attribution',
        'service_url',
        'publish'
    )
    list_filter = [
        'service_name',
        'service_id'
    ]
    search_fields = ['service_name', 'service_id', 'service_url']


admin.site.register(MapServices, MapServicesAdmin)
admin.site.register(LayerServices, LayerServicesAdmin)
