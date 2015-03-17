import os
import tempfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DEBUG = True
TEMPLATE_DEBUG = True

SECRET_KEY = 'test'

ROOT_URLCONF = 'livewatch.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

MIDDLEWARE_CLASSES = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',

    'celery',
    'djcelery',
    'django_rq',
    'livewatch',
)

STATIC_URL = '/'
MEDIA_URL = '/'

MEDIA_ROOT = tempfile.mkdtemp()

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    }
}

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
