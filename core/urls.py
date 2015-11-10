from django.conf.urls import patterns, include, url
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^user/', include('registration.backends.simple.urls')),
    url(r'^user/', include('django.contrib.auth.urls')),
    url(r'^destination/create/$', login_required(DestinationCreateView.as_view()), name='destination_create'),
    url(r'destination/$', login_required(DestinationListView.as_view()), name='destination_list'),
    url(r'^destination/(?P<pk>\d+)/$', login_required(DestinationDetailView.as_view()), name='destination_detail'),
    url(r'^destination/update/(?P<pk>\d+)/$', login_required(DestinationUpdateView.as_view()), name='destination_update'),
    url(r'^destination/delete/(?P<pk>\d+)/$', login_required(DestinationDeleteView.as_view()), name='destination_delete'),
    url(r'^destination/(?P<pk>\d+)/recommendation/create/$', login_required(RecommendationCreateView.as_view()), name='recommendation_create'),
    url(r'^destination/(?P<destination_pk>\d+)/recommendation/update/(?P<recommendation_pk>\d+)/$', login_required(RecommendationUpdateView.as_view()), name='recommendation_update'),
    url(r'^destination/(?P<destination_pk>\d+)/recommendation/delete/(?P<recommendation_pk>\d+)/$', login_required(RecommendationDeleteView.as_view()), name='recommendation_delete'),
)