from __future__ import absolute_import

import time
from datetime import datetime

import mock
from django.core.cache import cache

from ..extensions.rq import livewatch_update_rq_task
from ..tasks import livewatch_update_celery_task


class TestRqTask:
    key = 'livewatch_rq'

    def teardown(self):
        time.sleep(1)
        cache.delete(self.key)

    def test_livewatch_update_rq_task(self):
        assert cache.get(self.key) is None
        livewatch_update_rq_task(self.key)
        assert cache.get(self.key) is not None

    @mock.patch('livewatch.extensions.cache.cache.set')
    def test_livewatch_update_rq_task_cache_not_set(self, cache_mock):
        assert cache.get(self.key) is None
        livewatch_update_rq_task(self.key)
        assert cache.get(self.key) is None


class TestCeleryTask:
    key = 'livewatch_task'

    def teardown(self):
        time.sleep(1)
        cache.delete(self.key)

    def test_livewatch_update_celery_task(self):
        assert cache.get(self.key) is None
        livewatch_update_celery_task(self.key)
        assert isinstance(cache.get(self.key), datetime) is True
