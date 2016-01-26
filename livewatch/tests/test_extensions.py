from __future__ import absolute_import

import time
from datetime import timedelta

import mock
import pytest

from django.utils import timezone

from ..extensions.base import BaseExtension, TaskExtension
from ..extensions.cache import CacheExtension
from ..extensions.celery import CeleryExtension
from ..extensions.rq import RqExtension


class MockTaskExtension(TaskExtension):
    name = 'mock_task_extension'

    def run_task(self):
        return 'mock run task'


class TestBaseExtension:

    def test_check_service_not_implemented(self, rf):
        extension = BaseExtension()
        request = rf.get('/')

        with pytest.raises(NotImplementedError):
            extension.check_service(request)


class TestTaskExtension:
    key = 'livewatch_mock_task_extension'

    def test_run_task_not_implemented(self):
        extension = TaskExtension()

        with pytest.raises(NotImplementedError):
            extension.run_task()

    def test_check_service(self, cleared_cache, rf):
        time = timezone.now() - timedelta(minutes=5)
        cleared_cache.set(self.key, time, 2592000)

        request = rf.get('/')
        extension = MockTaskExtension()

        assert extension.check_service(request) is True

    def test_check_service_not_in_cache(self, rf):
        request = rf.get('/')
        extension = MockTaskExtension()

        assert extension.check_service(request) is False

    def test_check_service_timeout(self, cleared_cache, rf):
        time = timezone.now() - timedelta(minutes=16)
        cleared_cache.set(self.key, time, 2592000)

        request = rf.get('/')
        extension = MockTaskExtension()

        assert extension.check_service(request) is False


class TestCacheExtension:
    key = 'livewatch_cache'

    def test_check_service(self):
        extension = CacheExtension()

        assert extension.check_service() is True

    @mock.patch('livewatch.extensions.cache.cache.set')
    def test_check_service_not_active(self, cache_mock):
        extension = CacheExtension()
        assert extension.check_service() is False

    def test_check_service_cache_deleted_after_check(self, cleared_cache):
        extension = CacheExtension()

        assert extension.check_service() is True
        assert cleared_cache.get(self.key) is None


class TestRqExtension:
    key = 'livewatch_rq'

    def test_check_service(self, cleared_cache, rf, rq_worker):
        request = rf.get('/')
        extension = RqExtension()

        assert extension.check_service(request) is False
        time.sleep(1)
        assert extension.check_service(request) is True

    def test_check_service_not_in_cache(self, rf, cleared_cache):
        request = rf.get('/')
        extension = RqExtension()

        assert extension.check_service(request) is False
        assert extension.check_service(request) is False


class TestCeleryExtension:
    key = 'livewatch_celery'

    def test_check_service(self, rf, celery_worker, cleared_cache):
        request = rf.get('/')
        extension = CeleryExtension()

        assert extension.check_service(request) is False
        time.sleep(1)
        assert extension.check_service(request) is True

    def test_check_service_not_in_cache(self, rf, cleared_cache):
        request = rf.get('/')
        extension = CeleryExtension()

        assert extension.check_service(request) is False
        assert extension.check_service(request) is False
