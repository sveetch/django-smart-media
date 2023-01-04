.. _intro_install:

=======
Install
=======

Install package in your environment : ::

    pip install django-smart-media

For development usage see :ref:`install_development`.

Configuration
*************

Add it to your installed Django apps in settings : ::

    INSTALLED_APPS = (
        ...
        "smart_media",
    )

Then load default application settings in your settings file: ::

    from smart_media.settings import *

There is no migration to apply.

Settings
********

.. automodule:: smart_media.settings
   :members:
