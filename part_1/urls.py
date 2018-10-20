from django.conf.urls import url, include
from . import views

app_name = 'part_1'

urlpatterns = [
    url(r'^$', views.getKeys, name = 'getKeys'),
    url(r'^upload/$', views.simple_upload, name = 'form_upload')
]
