import re

from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import View


class LiveWatchView(View):

    def get(self, request, *args, **kwargs):
        if 'key' not in request.GET:
            return HttpResponse('Ok')

        if re.match(r'^[a-f0-9]{32}$', request.GET['key']):
            return HttpResponse(request.GET['key'])

        return HttpResponseNotFound()
