from __future__ import absolute_import

import mock
import pytest

from datetime import timedelta, datetime
from django.core.cache import cache
from django.utils import timezone


from ..extensions.base import BaseExtension, TaskExtension
from ..extensions.celery import CeleryExtension
from ..extensions.rq import RqExtension


class MockExtension(BaseExtension):
    name = 'mock_extension'

    def check_service(self, request):
        return 'mock check service'


class MockTaskExtension(TaskExtension):
    name = 'mock_task_extension'

    def check_service(self, request):
        return 'mock check service'

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
        cache.delete('livewatch_watchdog')

    def test_run_task(self):
        extension = MockTaskExtension()

        assert extension.run_task() == 'mock run task'

    def test_run_task_not_implemented(self):
        extension = TaskExtension()

        with pytest.raises(NotImplementedError):
            extension.run_task()

    @mock.patch('livewatch.extensions.base.TaskExtension.run_task')
    def test_check_service(self, run_task_mock, rf):
        time = timezone.now() - timedelta(minutes=5)
        cache.set('livewatch_watchdog', time, 2592000)

        request = rf.get('/')
        extension = TaskExtension()

        assert extension.check_service(request) is True

    @mock.patch('livewatch.extensions.base.TaskExtension.run_task')
    def test_check_service_cache_none(self, run_task_mock, rf):
        run_task_mock.return_value = None

        request = rf.get('/')
        extension = TaskExtension()

        assert extension.check_service(request) is False

    @mock.patch('livewatch.extensions.base.TaskExtension.run_task')
    def test_check_service_timeout(self, run_task_mock, rf):
        time = timezone.now() - timedelta(minutes=16)
        cache.set('livewatch_watchdog', time, 2592000)

        request = rf.get('/')
        extension = TaskExtension()

        assert extension.check_service(request) is False


class TestRqExtension:

    def setup(self):
        cache.delete('livewatch_watchdog')

    @mock.patch('livewatch.extensions.rq.django_rq.enqueue')
    def test_run_task(self, mock_task):
        extension = RqExtension()
        extension.run_task()

        assert mock_task.call_count == 1

    def test_livewatch_update_task(self):
        from ..extensions.rq import livewatch_update_task

        assert cache.get('livewatch_watchdog') is None
        livewatch_update_task()
        assert isinstance(cache.get('livewatch_watchdog'), datetime) is True


class TestCeleryExtension:

    def setup(self):
        cache.delete('livewatch_watchdog')

    @mock.patch('livewatch.extensions.celery.livewatch_update_task.delay')
    def test_run_task(self, mock_task):
        extension = CeleryExtension()
        extension.run_task()

        assert mock_task.call_count == 1
