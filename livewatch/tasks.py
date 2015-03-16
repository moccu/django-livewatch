import logging

from django.core.cache import cache
from django.utils import timezone


logger = logging.getLogger(__name__)


def livewatch_update_task():
    try:
        # livewatch view will check for this key, cache timeout: 30d
        cache.set('livewatch_watchdog', timezone.now(), 2592000)
        return True
    except:
        logger.error('Livewatch task failed.', exc_info=True)
        return False
