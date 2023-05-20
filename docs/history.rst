.. _intro_history:

=======
History
=======

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
