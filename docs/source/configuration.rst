Configuration
=============

LIVEWATCH_EXTENSIONS
--------------------

If you want to use it with ``django-celery`` or ``django-rq`` you have to update the ``LIVEWATCH_EXTENSIONS`` setting.

django-celery
`````````````

Make sure that you have ``celery`` installed. You can use the ``celery`` extra target for that.

.. code-block:: bash

    $ pip install django-livewatch[celery]

.. code-block:: python

    # Example with celery support
    LIVEWATCH_EXTENSIONS = (
        'livewatch.extensions.rq:CeleryExtension',
    )

django-rq
`````````

Make sure that you have ``rq`` installed. You can use the ``rq`` extra target for that.

.. code-block:: bash

    $ pip install django-livewatch[rq]

.. code-block:: python

    # Example with rq support
    LIVEWATCH_EXTENSIONS = (
        'livewatch.extensions.rq:RqExtension',
    )

For details on writing your own extensions, please see the :ref:`extending-livewatch` section.
