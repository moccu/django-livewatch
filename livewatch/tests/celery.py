from __future__ import absolute_import

from celery import Celery


celery = Celery(
    'livewatch', backend='redis://localhost:6379/2', broker='redis://localhost:6379/2')

celery.conf.update(
    CELERY_IMPORTS=('livewatch.tasks',),
    CELERY_ACCEPT_CONTENT=['pickle', 'json', 'msgpack', 'yaml'],
)
