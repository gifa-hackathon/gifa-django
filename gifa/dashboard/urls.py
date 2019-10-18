from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.gifa_dashboard, name='gifa_dashboard'),
    url(r'^disaster/$', views.panel_disaster, name = 'panel_disaster'),
    url(r'^dataviz/$', views.panel_visualization, name = 'panel_visualization'),
]
