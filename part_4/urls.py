from django.conf.urls import url, include
from . import views

app_name = 'part_4'

urlpatterns = [
    url(r'^$', views.requestfollow, name = 'sendRequest'),
]
