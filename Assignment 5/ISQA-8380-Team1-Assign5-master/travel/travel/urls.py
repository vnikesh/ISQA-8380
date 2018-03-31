from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('worldmap.urls', namespace='worldmap')),
    url(r'', include('thirdauth.urls', namespace='thirdauth')),
    url(r'^auth/', include('social_django.urls', namespace='social')),
]
