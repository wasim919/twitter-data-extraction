
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tweet/', include('part_1.urls'), name = 'tweet_upload'),
    url(r'^message/', include('part_2.urls'), name = 'messages'),
    url(r'^requestfollow/', include('part_4.urls'), name = 'requestfollowing'),
    url(r'^messagefollower/', include('part_3.urls'), name = 'messagefollower'),
    url(r'^$', views.home, name = 'home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
