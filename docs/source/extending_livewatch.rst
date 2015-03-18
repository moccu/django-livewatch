Extending Livewatch
===================

.. code-block:: python

    from livewatch.extensions.base import BaseExtension


    class FooBarExtension(BaseExtension):
        name = 'foo'

        def check_service(self, request):
            # check that service is running

