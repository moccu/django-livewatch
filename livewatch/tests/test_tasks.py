from __future__ import absolute_import

from datetime import datetime
from django.core.cache import cache

from ..tasks import livewatch_update_task


def test_livewatch_update_task():
    cache.delete('livewatch_watchdog')

    assert cache.get('livewatch_watchdog') is None
    livewatch_update_task()
    assert isinstance(cache.get('livewatch_watchdog'), datetime) is True
