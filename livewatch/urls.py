from __future__ import absolute_import

from django.conf.urls import patterns, url

from .views import LiveWatchView


urlpatterns = patterns(
    '',
    url(r'^$', LiveWatchView.as_view(), name='livewatch'),
    url(r'^(?P<service>\w+)/$', LiveWatchView.as_view(), name='livewatch-service'),
)
