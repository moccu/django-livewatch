from __future__ import absolute_import

import time

import django_rq
import mock
import pytest
from django.core.cache import cache

from django.core.urlresolvers import reverse

from .celery import celery
from ..utils import get_extensions


@pytest.mark.django_db
class TestLiveWatchView:

    def teardown(self):
        # Let all running tasks finish...
        time.sleep(1)

        # Purge celery queue...
        celery.control.purge()

        # Let the worker run in burst mode to clear the queue
        worker = django_rq.get_worker()
        worker.work(burst=True)

        # Let the worker finish...
        time.sleep(1)

        cache.delete('livewatch_cache')
        cache.delete('livewatch_rq')
        cache.delete('livewatch_celery')

    def test_url(self):
        assert '/' == reverse('livewatch')

    def test_url_service(self):
        expected_url = reverse('livewatch-service', kwargs={'service': 'testservice'})
        assert '/testservice/' == expected_url

    def test_get(self, client):
        url = reverse('livewatch')
        response = client.get(url)
        assert response.status_code == 200
        assert response.content == b'Ok'

    def test_get_key(self, client):
        url = reverse('livewatch')
        response = client.get('{0}?key={1}'.format(url, ('0' * 32)))
        assert response.status_code == 200
        assert response.content == (b'0' * 32)

    def test_get_key_error(self, client):
        url = reverse('livewatch')
        response = client.get('{0}?key={1}'.format(url, ('x' * 52)))
        assert response.status_code == 404
        assert response.content == b''

    def test_get_service_not_in_extensions(self, client):
        get_extensions(reload_extensions=True)
        url = reverse('livewatch-service', kwargs={'service': 'foobar'})
        response = client.get(url)
        assert response.status_code == 404
        assert response.content == b''

    def test_get_service_cache(self, client, settings):
        settings.LIVEWATCH_EXTENSIONS = ['livewatch.extensions.cache:CacheExtension']
        get_extensions(reload_extensions=True)

        url = reverse('livewatch-service', kwargs={'service': 'cache'})
        response = client.get(url)
        assert response.status_code == 200
        assert response.content == b'Ok'

    @mock.patch('livewatch.extensions.cache.cache.set')
    def test_get_service_cache_error(self, cache_mock, client, settings):
        settings.LIVEWATCH_EXTENSIONS = ['livewatch.extensions.cache:CacheExtension']
        get_extensions(reload_extensions=True)

        url = reverse('livewatch-service', kwargs={'service': 'cache'})
        response = client.get(url)
        assert response.status_code == 404
        assert response.content == b''

    def test_get_service_rq(self, client, settings, rq_worker):
        settings.LIVEWATCH_EXTENSIONS = ['livewatch.extensions.rq:RqExtension']
        get_extensions(reload_extensions=True)

        url = reverse('livewatch-service', kwargs={'service': 'rq'})
        response = client.get(url)

        assert response.status_code == 404
        assert response.content == b''

        time.sleep(1)
        response = client.get(url)

        assert response.status_code == 200
        assert response.content == b'Ok'

    def test_get_service_rq_error(self, client, settings):
        settings.LIVEWATCH_EXTENSIONS = ['livewatch.extensions.rq:RqExtension']
        get_extensions(reload_extensions=True)

        url = reverse('livewatch-service', kwargs={'service': 'rq'})
        response = client.get(url)
        assert response.status_code == 404
        assert response.content == b''

    def test_get_service_celery(self, client, settings, celery_worker):
        settings.LIVEWATCH_EXTENSIONS = ['livewatch.extensions.celery:CeleryExtension']
        get_extensions(reload_extensions=True)

        url = reverse('livewatch-service', kwargs={'service': 'celery'})
        response = client.get(url)

        assert response.status_code == 404
        assert response.content == b''

        time.sleep(1)
        response = client.get(url)

        assert response.status_code == 200
        assert response.content == b'Ok'

    def test_get_service_celery_error(self, client, settings):
        settings.LIVEWATCH_EXTENSIONS = ['livewatch.extensions.celery:CeleryExtension']
        get_extensions(reload_extensions=True)

        url = reverse('livewatch-service', kwargs={'service': 'celery'})
        response = client.get(url)
        assert response.status_code == 404
        assert response.content == b''
