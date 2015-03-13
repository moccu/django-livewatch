from django.conf.urls import patterns

from .views import livewatch


urlpatterns = patterns(
    '',
    (r'^$', livewatch),
)
