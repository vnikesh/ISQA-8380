from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^denver/$', views.denverText, name='denver'),
    url(r'^planner/$', views.plannerGetStarted, name='getStarted'),
    url(r'^accounts/profile/$', views.home, name='profile'),
]