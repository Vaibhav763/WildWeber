from . import views
from django.urls import path, re_path
from django.conf.urls import url

app_name = 'accounts'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^explore/$', views.explore, name='explore'),
    url(r'^privacy/$', views.privacy, name='privacy'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^othersprofile/$', views.othersprofile, name='othersprofile'),
    url(r'team', views.team, name='team'),
    url(r'terms', views.terms, name='terms'),
    url(r'verification', views.verification, name='verification'),
    url(r'feedback', views.feedback, name='feedback'),
    url(r'password', views.password, name='password'),

    re_path(r'^loginbase/$',views.loginbase,name='loginbase'),
    re_path(r'^registerbase/$',views.registerbase,name='registerbase'),
]
