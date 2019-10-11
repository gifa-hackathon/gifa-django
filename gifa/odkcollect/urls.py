from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^geojson', views.get_odk_geojson, name='get_odk_geojson'),
]
