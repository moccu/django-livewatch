from __future__ import absolute_import

import time
from datetime import timedelta

import mock
import pytest
import django_rq
from django.core.cache import cache, caches
from django.utils import timezone

from .celery import celery
from ..extensions.base import BaseExtension, TaskExtension
from ..extensions.cache import CacheExtension
from ..extensions.celery import CeleryExtension
from ..extensions.rq import RqExtension


class MockExtension(BaseExtension):
    name = 'mock_extension'

    def check_service(self, request):
        return 'mock check service'


class MockTaskExtension(TaskExtension):
    name = 'mock_task_extension'

    def run_task(self):
        return 'mock run task'


class TestBaseExtension:

    def test_check_service(self, rf):
        extension = MockExtension()
        request = rf.get('/')

        assert extension.check_service(request) == 'mock check service'

    def test_check_service_not_implemented(self, rf):
        extension = BaseExtension()
        request = rf.get('/')

        with pytest.raises(NotImplementedError):
            extension.check_service(request)


class TestTaskExtension:

    def setup(self):
        self.key = 'livewatch_mock_task_extension'
        cache.delete(self.key)

    def teardown(self):
        cache.delete(self.key)

    def test_run_task(self):
        extension = MockTaskExtension()

        assert extension.run_task() == 'mock run task'

    def test_run_task_not_implemented(self):
        extension = TaskExtension()

        with pytest.raises(NotImplementedError):
            extension.run_task()

    def test_check_service(self, rf):
        time = timezone.now() - timedelta(minutes=5)
        cache.set(self.key, time, 2592000)

        request = rf.get('/')
        extension = MockTaskExtension()

        assert extension.check_service(request) is True

    def test_check_service_not_in_cache(self, rf):
        request = rf.get('/')
        extension = MockTaskExtension()

        assert extension.check_service(request) is False

    def test_check_service_timeout(self, rf):
        time = timezone.now() - timedelta(minutes=16)
        cache.set(self.key, time, 2592000)

        request = rf.get('/')
        extension = MockTaskExtension()

        assert extension.check_service(request) is False


class TestCacheExtension:

    def setup(self):
        self.key = 'livewatch_cache'

    def teardown(self):
        cache.delete(self.key)

    def test_check_service(self):
        extension = CacheExtension()

        assert extension.check_service() is True

    @mock.patch('livewatch.extensions.cache.cache.get')
    def test_check_service_not_active(self, cache_mock):
        cache_mock.return_value = None

        extension = CacheExtension()

        assert extension.check_service() is False

    def test_check_service_cache_deleted_after_check(self):
        extension = CacheExtension()

        assert extension.check_service() is True
        assert cache.get(self.key) is None


class TestRqExtension:

    def setup(self):
        self.key = 'livewatch_rq'
        # cache.delete(self.key)
        # Reset django cache caching :-D
        caches._caches.caches = {}

    def teardown(self):
        # Let all running tasks finish...
        time.sleep(1)

        # Let the worker run in burst mode to clear the queue
        worker = django_rq.get_worker()
        worker.work(burst=True)

        # Let the worker finish...
        time.sleep(1)

        # Cleanup cache key used in tests
        cache.delete(self.key)

        # Reset django cache caching :-D
        caches._caches.caches = {}

    def test_check_service(self, rf, rq_worker):
        request = rf.get('/')
        extension = RqExtension()

        assert extension.check_service(request) is False
        time.sleep(1)
        assert extension.check_service(request) is True

    def test_check_service_not_in_cache(self, rf):
        request = rf.get('/')
        extension = RqExtension()

        assert extension.check_service(request) is False
        assert extension.check_service(request) is False

    def test_livewatch_update_task(self):
        from ..extensions.rq import livewatch_update_task

        assert cache.get(self.key) is None
        livewatch_update_task(self.key)
        assert cache.get(self.key) is not None

    def test_livewatch_update_task_cache_not_set(self, settings):
        settings.CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            }
        }

        from ..extensions.rq import livewatch_update_task

        assert cache.get(self.key) is None
        livewatch_update_task(self.key)
        assert cache.get(self.key) is None


class TestCeleryExtension:

    def setup(self):
        self.key = 'livewatch_celery'

    def teardown(self):
        # Let all running tasks finish...
        time.sleep(1)

        # Purge celery queue...
        celery.control.purge()

        # Let the worker finish...
        time.sleep(1)

        cache.delete(self.key)

    def test_check_service(self, rf, celery_worker):
        request = rf.get('/')
        extension = CeleryExtension()

        assert extension.check_service(request) is False
        time.sleep(1)
        assert extension.check_service(request) is True

    def test_check_service_not_in_cache(self, rf):
        request = rf.get('/')
        extension = CeleryExtension()

        assert extension.check_service(request) is False
        assert extension.check_service(request) is False
