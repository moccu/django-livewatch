import logging

from django.core.cache import cache

from .base import BaseExtension

logger = logging.getLogger(__name__)


class CacheExtension(BaseExtension):
    name = 'cache'

    def check_service(self, request):
        cache.set('livewatch_watchdog', 'cache_activated')

        watchdog = cache.get('livewatch_watchdog')
        if watchdog == 'cache_activated':
            return True

        return False
