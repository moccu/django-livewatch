from __future__ import absolute_import

import mock
import pytest

from django.core.urlresolvers import reverse

from ..utils import get_extensions


@pytest.mark.django_db
class TestLiveWatchView:

    def test_url(self):
        assert '/' == reverse('livewatch')

    def test_url_service(self, settings):
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

    @mock.patch('livewatch.extensions.rq.RqExtension.check_service')
    def test_get_service_rq(self, service_mock, client, settings):
        settings.LIVEWATCH_EXTENSIONS = ['livewatch.extensions.rq:RqExtension']
        get_extensions(reload_extensions=True)
        service_mock.return_value = True

        url = reverse('livewatch-service', kwargs={'service': 'rq'})
        response = client.get(url)
        assert response.status_code == 200
        assert response.content == b'Ok'

    @mock.patch('livewatch.extensions.rq.RqExtension.check_service')
    def test_get_service_rq_error(self, service_mock, client, settings):
        settings.LIVEWATCH_EXTENSIONS = ['livewatch.extensions.rq:RqExtension']
        get_extensions(reload_extensions=True)
        service_mock.return_value = False

        url = reverse('livewatch-service', kwargs={'service': 'rq'})
        response = client.get(url)
        assert response.status_code == 404
        assert response.content == b''
