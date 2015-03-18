from __future__ import absolute_import

import logging

from django.core.cache import cache
from django.utils import timezone

from .celery import celery


logger = logging.getLogger(__name__)


@celery.task
def livewatch_update_task():
    try:
        # livewatch view will check for this key, cache timeout: 30d
        cache.set('livewatch_watchdog', timezone.now(), 2592000)
        return True
    except Exception as exc:
        logger.error(
            'Livewatch task failed. {0}: {1}'.format(
                exc.__class__.__name__, exc)
        )

        return False
