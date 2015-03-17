from __future__ import absolute_import

import mock

from datetime import datetime
from django.core.cache import cache
from django.test.utils import patch_logger

from ..tasks import livewatch_update_task


def test_livewatch_update_task():
    cache.delete('livewatch_watchdog')

    assert cache.get('livewatch_watchdog') is None

    assert livewatch_update_task() is True
    assert isinstance(cache.get('livewatch_watchdog'), datetime) is True


@mock.patch('livewatch.tasks.cache.set')
def test_livewatch_update_task_error(cache_mock):
    cache_mock.side_effect = Exception
    cache.delete('livewatch_watchdog')

    with patch_logger('livewatch.tasks', 'error') as calls:
        assert livewatch_update_task() is False
        assert len(calls) == 1

    assert cache.get('livewatch_watchdog') is None
