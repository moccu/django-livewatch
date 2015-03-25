from __future__ import absolute_import

from celery import Celery


celery = Celery(
    'livewatch', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')

celery.conf.update(
    CELERY_IMPORTS=('livewatch.tasks',),
)
