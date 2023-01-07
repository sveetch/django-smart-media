.. _Python: https://www.python.org/
.. _Django: https://www.djangoproject.com/
.. _sorl-thumbnail: https://github.com/jazzband/sorl-thumbnail

==================
Django smart media
==================

A suit of tools to use a FileField to upload image with light SVG support, include
thumbnail preview in field and a template tag around `sorl-thumbnail`_ library.


Dependancies
************

* `Python`_>=3.8;
* `Django`_>=3.2,<4.2;
* `sorl-thumbnail`_>=12.9.0;


Overview
********

Concretely this contains:

* Form widgets to build HTML for a ``FileField`` either with or without clearable
  mode. Both mode have a version to include needed layout assets (CSS and Javascript)
  and another one without assets;
* Templates to build the widgets HTML;
* CSS and Javascript for the widget layout;
* Form fields which already set a "smart" widget;
* Field validator;
* Model signals to purge stale files;
* Model field with all "smart" features;
* A template tag to make a thumbnail that can be used either in the form for preview
  or to be used in frontend for content thumbnail. By default, the thumbnail is
  made in the original content format. Also not than a SVG cannot be converted to a
  Bitmap and vice versa;
* Some helpers to ease some specific implementations;

Although this can work with ``ImageField``, SVG support will only work with
``FileField`` since ``ImageField`` rely on PIL that does not support SVG format.


Links
*****

* Read the documentation on `Read the docs <https://django-smart-media.readthedocs.io/>`_;
* Download its `PyPi package <https://pypi.python.org/pypi/django-smart-media>`_;
* Clone it on its `Github repository <https://github.com/sveetch/django-smart-media>`_;
