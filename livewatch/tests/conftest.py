from __future__ import absolute_import

import pytest
import time

import django_rq
from celery.signals import worker_ready

from .celery import celery


WORKER_READY = list()


@worker_ready.connect
def on_worker_ready(**kwargs):
    """Called when the Celery worker thread is ready to do work.
    This is to avoid race conditions since everything is in one python process.
    """
    WORKER_READY.append(True)


@pytest.yield_fixture
def celery_worker(request):
    """Fixture starting a celery worker in background"""

    from multiprocessing import Process

    celery_args = ['-C', '-q', '-c', '1', '-P', 'solo', '--without-gossip', '--loglevel=fatal']
    proc = Process(target=lambda: celery.worker_main(celery_args))

    proc.start()

    # Wait for worker to finish initializing to avoid a race condition I've been experiencing.
    for i in range(5):
        if WORKER_READY:
            break
        time.sleep(1)

    yield proc

    proc.terminate()

    time.sleep(1)


@pytest.yield_fixture
def rq_worker(request):
    """Fixture starting a rq worker in background"""

    from multiprocessing import Process

    def _proc_target(env):
        import os
        os.environ.update(env)
        worker = django_rq.get_worker()
        worker.work()

    proc = Process(target=_proc_target, kwargs={
        'env': {'DJANGO_SETTINGS_MODULE': 'livewatch.tests.settings'}
    })

    proc.start()

    time.sleep(1)

    yield proc

    proc.terminate()

    time.sleep(1)
