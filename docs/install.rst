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

Then mount applications URLs: ::

    urlpatterns = [
        ...
        path("", include("smart_media.urls")),
    ]

And finally apply database migrations.

Settings
********

.. automodule:: smart_media.settings
   :members:
