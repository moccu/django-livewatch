import logging

import django_rq
from django.core.cache import cache
from django.utils import timezone

from .base import Extension


logger = logging.getLogger(__name__)


def livewatch_update_task():
    try:
        # livewatch view will check for this key, cache timeout: 30d
        cache.set('livewatch_watchdog', timezone.now(), 2592000)
        return True
    except Exception:
        logger.error('Livewatch task failed.', exc_info=True)
        return False


class RqExtension(Extension):
    name = 'rq'

    def check_service(self, request):
        django_rq.enqueue(livewatch_update_task)
        watchdog_timestamp = cache.get('livewatch_watchdog')
        if watchdog_timestamp is None:
            return False

        watchdog_timeout = int(request.GET.get('timeout', 900))
        watchdog_timestamp_diff = (timezone.now() - watchdog_timestamp)
        watchdog_timestamp_diff = (
            watchdog_timestamp_diff.seconds + watchdog_timestamp_diff.days * 24 * 3600)

        if watchdog_timestamp_diff > watchdog_timeout:
            return False

        return True
