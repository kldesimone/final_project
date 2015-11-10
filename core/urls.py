from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^user/', include('registration.backends.simple.urls')),
    url(r'^user/', include('django.contrib.auth.urls')),
    url(r'^destination/create/$', DestinationCreateView.as_view(), name='destination_create'),
    url(r'destination/$', DestinationListView.as_view(), name='destination_list'),
    url(r'^destination/(?P<pk>\d+)/$', DestinationDetailView.as_view(), name='destination_detail'),
    url(r'^destination/update/(?P<pk>\d+)/$', DestinationUpdateView.as_view(), name='destination_update'),
    url(r'^destination/delete/(?P<pk>\d+)/$', DestinationDeleteView.as_view(), name='destination_delete'),
    url(r'^destination/(?P<pk>\d+)/recommendation/create/$', RecommendationCreateView.as_view(), name='recommendation_create'),
    url(r'^destination/(?P<destination_pk>\d+)/recommendation/update/(?P<recommendation_pk>\d+)/$', RecommendationUpdateView.as_view(), name='recommendation_update'),
    url(r'^destination/(?P<destination_pk>\d+)/recommendation/delete/(?P<recommendation_pk>\d+)/$', RecommendationDeleteView.as_view(), name='recommendation_delete'),
)