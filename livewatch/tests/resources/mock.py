from __future__ import absolute_import


from ...extensions.base import BaseExtension, TaskExtension


class MockExtension(BaseExtension):
    name = 'mock_extension'

    def check_service(self, request):
        return 'mock check service'


class MockTaskExtension(TaskExtension):
    name = 'mock_task_extension'

    def check_service(self, request):
        return 'mock check service'

    def run_task(self):
        return 'mock run task'
