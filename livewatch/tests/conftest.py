from __future__ import absolute_import
import os
import signal

import pytest
import time

import django_rq
from celery.signals import worker_ready
from django.core.cache import cache

from .celery import celery


CELERY_WORKER_READY = list()


@worker_ready.connect
def on_worker_ready(**kwargs):
    """Called when the Celery worker thread is ready to do work.
    This is to avoid race conditions since everything is in one python process.
    """
    CELERY_WORKER_READY.append(True)


@pytest.yield_fixture
def cleared_cache(request):
    cache.clear()

    yield cache

    cache.clear()


@pytest.yield_fixture
def celery_worker(request):
    """Fixture starting a celery worker in background"""
    from multiprocessing import Process

    # Always clear the queue first
    celery.control.purge()

    celery_args = ['-C', '-q', '-l', 'FATAL', '-c', '1', '-P', 'solo', '--without-gossip']
    proc = Process(target=lambda: celery.worker_main(celery_args))

    proc.start()

    # Wait for worker to finish initializing to avoid a race condition I've been experiencing.
    for i in range(5):
        if CELERY_WORKER_READY:
            break
        time.sleep(1)

    yield proc

    proc.terminate()
    proc.join(10)

    try:
        os.kill(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass

    celery.control.purge()

    del CELERY_WORKER_READY[:]


@pytest.yield_fixture
def rq_worker(request):
    """Fixture starting a rq worker in background"""
    from multiprocessing import Process

    # First clear the queue
    [queue.empty() for queue in django_rq.get_worker().queues]

    def _proc_target(env):
        import os
        os.environ.update(env)
        worker = django_rq.get_worker()
        worker.work()

    proc = Process(target=_proc_target, kwargs={
        'env': {'DJANGO_SETTINGS_MODULE': 'livewatch.tests.settings'}
    })
    proc.start()

    while not proc.is_alive():
        time.sleep(1)

    yield proc

    # Wait for rq to exit, timeout 5 seconds.
    proc.terminate()
    proc.join(10)

    try:
        os.kill(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass

    [queue.empty() for queue in django_rq.get_worker().queues]
