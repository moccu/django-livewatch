import mock
import pytest

from datetime import datetime, timedelta
from django.core.cache import cache
from django.utils import timezone

from livewatch.extensions.base import Extension
from livewatch.extensions.rq import RqExtension
from livewatch.tasks import livewatch_update_task


class TestBaseExtension:

    def test_check_not_implemented(self, rf):
        ext = Extension()
        request = rf.get('/')

        with pytest.raises(NotImplementedError):
            ext.check(request)


class TestRqExtension:

    def setup(self):
        cache.delete('livewatch_watchdog')

    def test_livewatch_update_task(self):
        assert cache.get('livewatch_watchdog') is None

        livewatch_update_task()
        assert isinstance(cache.get('livewatch_watchdog'), datetime) is True

    @mock.patch('livewatch.tasks.cache.set')
    def test_livewatch_update_task_error(self, cache_mock):
        cache_mock.side_effect = Exception

        assert livewatch_update_task() is False
        assert cache.get('livewatch_watchdog') is None

    def test_check_service(self, rf):
        time = timezone.now() - timedelta(minutes=5)
        cache.set('livewatch_watchdog', time, 2592000)

        request = rf.get('/')
        rq = RqExtension()

        assert rq.check_service(request) is True

    @mock.patch('livewatch.extensions.rq.django_rq.enqueue')
    def test_check_service_cache_none(self, service_mock, rf):
        service_mock.return_value = None

        request = rf.get('/')
        rq = RqExtension()

        assert rq.check_service(request) is False

    @mock.patch('livewatch.extensions.rq.django_rq.enqueue')
    def test_check_service_timeout(self, service_mock, rf):
        time = timezone.now() - timedelta(minutes=16)
        cache.set('livewatch_watchdog', time, 2592000)

        request = rf.get('/')
        rq = RqExtension()

        assert rq.check_service(request) is False
