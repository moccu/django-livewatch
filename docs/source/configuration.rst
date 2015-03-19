Configuration
=============

LIVEWATCH_EXTENSIONS
--------------------

If you want to use it with ``django-celery`` or ``django-rq`` you have to update the ``LIVEWATCH_EXTENSIONS`` setting.

django-celery
`````````````
.. code-block:: python

    # Example with celery support
    LIVEWATCH_EXTENSIONS = (
        'livewatch.extensions.rq:CeleryExtension',
    )

django-rq
`````````
.. code-block:: python

    # Example with rq support
    LIVEWATCH_EXTENSIONS = (
        'livewatch.extensions.rq:RqExtension',
    )

For details on writing your own extensions, please see the :ref:`extending-livewatch` section.
