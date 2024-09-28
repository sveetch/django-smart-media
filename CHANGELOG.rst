=========
Changelog
=========

Version 0.4.1 - 2024/09/28
--------------------------

A minor release just to fix issue with Read the Docs configuration that failed to
build.


Version 0.4.0 - 2024/09/28
--------------------------

.. Note::
    If you are still using Django 4.0 or 4.1 you will need to pin sorl-thumbnail to
    ``sorl-thumbnail==12.10.0`` in your project requirements because last Sorl release
    have dropped support of Django<4.2 and Smart media does not pin it (since it is
    compatible with every versions).

* Removed support for Django<4.0;
* Added support for Django 5.0 and 5.1;
* Storage class usage has been adapted to ensure compatibility for Django from 4.0 to
  5.0;
* Added a minimal version to every requirements to help Pip to resolve packages
  quicker;
* Added a logo;
* Upgraded documentation to Furo theme;
* Updated script to freeze local dependencies;


Version 0.3.1 - 2023/08/18
--------------------------

* Updated ``.readthedocs.yml`` file to follow service deprecations changes;
* Added a warning about purge signals in documentation;


Version 0.3.0 - 2023/04/04
--------------------------

* Added support for Django 4.2;
* This will be the last version to support Django 3.2;
* Added missing link to Sorl documentation in tag docstring, close #5;
* Fixed invisible thumb for SVG file in preview from ``FileInputButtonBase`` widget,
  close #9;
* Removed last jQuery usage from Javascript code so it is full vanilla Javascript and
  it is compatible anywhere, close #1;
* Changed field name ``media`` to ``mediafile`` in model and forms from sample
  application since ``media`` is an used form attribute to get form medias;
* Added a view in sample application just to render form ``ImageItemFieldsForm``
  without model;
* Added Tutorial document, close #6;
* Added ``SmartAdminMixin`` to use instead of ``SmartModelAdmin`` when model admin to
  inherit from another subclass of ``ModelAdmin`` close #11;
* Improved references document;


Version 0.2.2 - 2023/04/04
--------------------------

* Added ``smart_media.contrib.django_configuration.SmartMediaDefaultSettings`` class to
  use with  `django-configuration <https://django-configurations.readthedocs.io/en/stable/>`_
  to include default settings instead of ``from smart_media.settings import *``;
* Improved installation document;
* Fixed some typos from docstrings;


Version 0.2.1 - 2023/01/11
--------------------------

Fixed documentation build on RTFD.


Version 0.2.0 - 2023/01/11
--------------------------

* Added a model field;
* Added Model admin;
* Added purge signals;
* Finished documentation;
* Finished test coverage;


Version 0.1.0 - 2022/12/29
--------------------------

First commit.
