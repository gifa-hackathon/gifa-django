from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.gifa_dashboard, name='gifa_dashboard'),
    url(r'^affected_family/$', views.panel_affected_family, name = 'panel_affected_family'),
    url(r'^shelter/$', views.panel_shelter, name = 'panel_shelter'),
    url(r'^dataviz/$', views.panel_visualization, name = 'panel_visualization'),
]
