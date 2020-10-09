from accounts import views
from django.conf.urls import url
from django.conf.urls import include

urlpatterns = [
    url (r'^about/$', views.about, name='about'),
    url (r'^explore/$', views.explore, name='explore'),
    url (r'^privacy/$', views.privacy, name='privacy'),
    url (r'^signup/$', views.signup, name='signup'),
    url (r'^othersprofile/$', views.othersprofile, name='othersprofile'),
    url (r'team', views.team, name='team'),

    url(r'^$',views.index,name='index'),
]
