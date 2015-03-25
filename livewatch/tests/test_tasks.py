from __future__ import absolute_import

import time
from datetime import datetime

from django.core.cache import cache

from ..tasks import livewatch_update_task


class TestTask:

    def setup(self):
        self.key = 'livewatch_task'

    def teardown(self):
        time.sleep(.2)
        cache.delete(self.key)

    def test_livewatch_update_task(self):
        assert cache.get(self.key) is None
        livewatch_update_task(self.key)
        assert isinstance(cache.get(self.key), datetime) is True
