from django.core.cache import cache
from django.utils import timezone


class BaseExtension(object):
    name = None

    def check_service(self, request):
        raise NotImplementedError


class TaskExtension(BaseExtension):
    name = 'taskextension'

    def check_service(self, request):
        key = 'livewatch_{0}'.format(self.name)

        # Fetch timestamp before inserting task.
        watchdog_timestamp = cache.get(key)

        self.run_task()

        if watchdog_timestamp is None:
            return False

        watchdog_timeout = int(request.GET.get('timeout', 900))
        watchdog_timestamp_diff = (timezone.now() - watchdog_timestamp)
        watchdog_timestamp_diff = (
            watchdog_timestamp_diff.seconds + watchdog_timestamp_diff.days * 24 * 3600)

        if watchdog_timestamp_diff > watchdog_timeout:
            return False

        return True

    def run_task(self):
        raise NotImplementedError
