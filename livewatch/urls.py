from django.conf.urls import patterns, url

from .views import LiveWatchView


urlpatterns = patterns(
    '',
    url(r'^$', LiveWatchView.as_view(), name='livewatch'),
)
