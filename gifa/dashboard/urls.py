from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.gifa_dashboard, name='gifa_dashboard'),
    url(r'^affected_family/$', views.panel_affected_family, name = 'panel_affected_family'),
    url(r'^humanitarian_aid/$', views.panel_humanitarian_aid, name = 'panel_humanitarian_aid'),
    url(r'^dataviz/$', views.panel_visualization, name = 'panel_visualization'),
    url(r'^vulnerability/$', views.panel_vulnerability, name = 'panel_vulnerability'),
    url(r'^exposure/$', views.panel_exposure, name = 'panel_exposure'),
]
