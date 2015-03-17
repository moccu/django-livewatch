from __future__ import absolute_import

from django.test.utils import patch_logger

from ..extensions.rq import RqExtension
from ..utils import get_extensions


def test_get_extensions(settings):
    settings.LIVEWATCH_EXTENSIONS = ['livewatch.extensions.rq:RqExtension']

    extensions = get_extensions(reload_extensions=True)
    assert len(extensions) == 1
    assert 'rq' in extensions
    assert isinstance(extensions['rq'], RqExtension)


def test_get_extensions_error(settings):
    settings.LIVEWATCH_EXTENSIONS = ['livewatch.extensions.foo:BarExtension']

    with patch_logger(
            'livewatch.utils', 'error') as calls:
        get_extensions(reload_extensions=True)

        assert len(calls) == 1
        assert calls[0] == 'Failed to import livewatch.extensions.foo:BarExtension'
