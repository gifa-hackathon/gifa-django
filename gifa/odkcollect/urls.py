from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^geojson/(?P<con_id>[\w-]+)', views.get_odk_geojson, name='get_odk_geojson'),
]
