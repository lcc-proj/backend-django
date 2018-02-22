from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.index),
    url(r'rejeitar/(?P<pk>\d+)/$', views.rejeitar),
    url(r'aprovar/(?P<pk>\d+)/$', views.aprovar),
    url(r'aprovar_com_replanejamento/(?P<pk>\d+)/$', views.aprovar_com_replanejamento),
    url(r'^(?P<pk>\d+)/versao/(?P<codigo_versao>\d+)/$', views.index),
    url(r'api/postits/$', views.api_postits_canvas),
]