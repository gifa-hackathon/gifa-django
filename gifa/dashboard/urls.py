from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.gifa_dashboard, name='gifa_dashboard'),
    url(r'^dashboard2', views.gifa_dashboard2, name='gifa_dashboard2'),
]