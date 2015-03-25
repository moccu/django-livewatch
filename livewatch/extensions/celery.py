from __future__ import absolute_import

from .base import TaskExtension
from ..tasks import livewatch_update_task


class CeleryExtension(TaskExtension):
    name = 'celery'

    def run_task(self):
        key = 'livewatch_{0}'.format(self.name)
        livewatch_update_task.delay(key)
