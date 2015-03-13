import re

from django.http import HttpResponse, HttpResponseNotFound


def livewatch(request):
    if 'key' not in request.REQUEST:
        return HttpResponse('Ok')

    if re.match(r'^[a-f0-9]{32}$', request.REQUEST['key']):
        return HttpResponse(request.REQUEST['key'])

    return HttpResponseNotFound()
