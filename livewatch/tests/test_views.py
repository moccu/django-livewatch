import mock
import pytest

from django.core.urlresolvers import reverse


@pytest.mark.django_db
class TestLiveWatchView:

    def test_url(self):
        assert '/' == reverse('livewatch')

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

    def test_url_rq(self, settings):
        assert '/rq/' == reverse('livewatch-service', kwargs={'service': 'rq'})

    @mock.patch('livewatch.extensions.rq.django_rq.enqueue')
    def test_get_service_error(self, service_mock, client, settings):
        settings.LIVEWATCH_EXTENSIONS = ['livewatch.extensions.rq:RqExtension']
        service_mock.return_value = None

        url = reverse('livewatch-service', kwargs={'service': 'rq'})
        response = client.get(url)
        assert response.status_code == 404
        assert response.content == b''
