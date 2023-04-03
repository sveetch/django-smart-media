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
        "sorl.thumbnail",
        "smart_media",
    )

.. Note::

    There may be conflicts if your project use also the "easy-thumbnail"
    library. To avoid this you should put the lines with ``sorl.thumbnail`` and
    ``smart_media`` just after the Django builtin apps and always before
    "easy-thumbnail";

Then load default application settings in your settings file: ::

    from smart_media.settings import *

.. Note::

    Instead, if your project use
    `django-configuration <https://django-configurations.readthedocs.io/en/stable/>`_,
    your settings class can inherits from
    ``smart_media.contrib.django_configuration.SmartMediaDefaultSettings`` (see it in
    :ref:`references_contrib`).

There is no migration to apply for this application.


Settings
********

.. automodule:: smart_media.settings
   :members:
