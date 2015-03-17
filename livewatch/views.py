from __future__ import absolute_import

import re
import importlib
import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import View

logger = logging.getLogger(__name__)


class LiveWatchView(View):

    def get_extensions(self):
        extensions = {}
        registered = getattr(settings, 'LIVEWATCH_EXTENSIONS', [])

        for extension in registered:
            try:
                base, cls = extension.split(':', 1)
                module = importlib.import_module(base)
                extension_class = getattr(module, cls)
                extensions[extension_class.name] = extension_class()
            except ImportError:
                logger.error('Failed to import {0}'.format(extension))
        return extensions

    def get(self, request, *args, **kwargs):
        extensions = self.get_extensions()

        service = kwargs.get('service', None)
        if service and service in extensions:
            retval = extensions[service].check_service(request)
            if not retval:
                return HttpResponseNotFound()

        if 'key' not in request.GET:
            return HttpResponse('Ok')

        if re.match(r'^[a-f0-9]{32}$', request.GET['key']):
            return HttpResponse(request.GET['key'])

        return HttpResponseNotFound()
