from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.index),
    url(r'^(?P<pk>\d+)/versao/(?P<codigo_versao>\d+)/$', views.index),
    url(r'^api/postits/$', views.api_postits_canvas),
]