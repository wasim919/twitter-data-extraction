from django.conf.urls import url, include
from . import views

app_name = 'part_2'

urlpatterns = [
    url(r'^$', views.sendMessage, name = 'sendMessage'),
    url(r'^comment/$', views.sendComment, name = 'commenting')
]
