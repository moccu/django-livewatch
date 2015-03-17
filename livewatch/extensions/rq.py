from __future__ import absolute_import

import django_rq

from .base import TaskExtension
from ..tasks import livewatch_update_task


class RqExtension(TaskExtension):
    name = 'rq'

    def run_task(self):
        django_rq.enqueue(livewatch_update_task())
