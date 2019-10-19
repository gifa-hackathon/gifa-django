from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.gifa_dashboard, name='gifa_dashboard'),
    url(r'^affected_family/$', views.panel_affected_family, name = 'panel_affected_family'),
    url(r'^humanitarian_aid/$', views.panel_humanitarian_aid, name = 'panel_humanitarian_aid'),
    url(r'^dataviz/$', views.panel_visualization, name = 'panel_visualization'),
]
