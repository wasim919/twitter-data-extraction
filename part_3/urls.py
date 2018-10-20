from django.conf.urls import url, include
from . import views

app_name = 'part_3'

urlpatterns = [
    url(r'^$', views.sendFollowerMessage, name = 'sendFollowerMessage'),
    url(r'^comment/$', views.sendFollowerComment, name = 'commentingfollower')
]
