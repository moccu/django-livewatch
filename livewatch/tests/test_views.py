import pytest


@pytest.mark.django_db
class TestLiveWatchView:
    def test_get(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert response.content == b'Ok'

    def test_get_key(self, client):
        response = client.get('/?key=%s' % ('0' * 32))
        assert response.status_code == 200
        assert response.content == (b'0' * 32)

    def test_get_key_error(self, client):
        response = client.get('/?key=%s' % ('x' * 52))
        assert response.status_code == 404
        assert response.content == b''
