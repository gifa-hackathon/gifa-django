from django.contrib import admin

from mapservice.models import MapServices, LayerServices


admin.site.register(MapServices)
admin.site.register(LayerServices)
