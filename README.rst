django-livewatch
================

.. image:: https://badge.fury.io/py/django-livewatch.png
    :target: http://badge.fury.io/py/django-livewatch

.. image:: https://travis-ci.org/moccu/django-livewatch.png?branch=master
    :target: https://travis-ci.org/moccu/django-livewatch

.. image:: https://readthedocs.org/projects/django-livewatch/badge/?version=latest
    :target: http://django-livewatch.readthedocs.org/en/latest/

livewatch.de integration for django projects


Installation
============

* Install ``django-livewatch`` (or `download from PyPI <http://pypi.python.org/pypi/django-livewatch>`_):

.. code-block:: python

    pip install django-livewatch

* Add ``livewatch`` to ``INSTALLED_APPS`` in ``settings.py``:

.. code-block:: python

    INSTALLED_APPS = (
        # other apps
        'livewatch',
    )

* Include ``livewatch.urls`` in your ``urls.py``:

.. code-block:: python

    urlpatterns += patterns('',
        (r'^livewatch/', include('livewatch.urls')),
    )

Resources
=========

* `Documentation <https://django-livewatch.readthedocs.org/>`_
* `Bug Tracker <https://github.com/moccu/django-livewatch/issues>`_
* `Code <https://github.com/moccu/django-livewatch/>`_
