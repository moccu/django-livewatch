from __future__ import absolute_import

from celery import Celery
from django.conf import settings


celery = Celery('livewatch')

celery.config_from_object('django.conf:settings')
celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS, related_name='tasks')
