.. _intro_references:

==========
References
==========

Preview
*******

Any field which use the widget ``ClearableFileInputButton`` would have a specific
look when editing.

.. figure:: /_static/ClearableFileInputButton.png
   :align: center

   Input got existing image preview with a checkbox to clear field value (and remove
   related file).

Obviously, there won't be any preview or clear checkbox when field is empty. In this
case only the upload button will be showed.


Widgets
*******

Widgets are just about HTML and layout, nothing more. There are different widgets so use
the one which fullfil your needs but to know ``ClearableFileInputButton`` is the most
featured one.

Commonly you will not use the ``***Base`` ones except in some context where you need to
load stylesheets and Javascript assets on your own.

.. automodule:: smart_media.widgets
   :members:


Form Fields
***********

Form fields implement widgets for ``FileField`` and ``ImageField`` but they are less
easy to use with a model form.

.. automodule:: smart_media.fields
   :members:


Model Fields
************


.. automodule:: smart_media.modelfields
   :members:


Model signals
*************

These signals are not mandatory but are very helpful to automatically clean your media
directory from stall files.

They are on your own to implement in your models still it is very easy to do and do
not require any migrations.


.. automodule:: smart_media.signals
   :members:


Django admin
************


.. automodule:: smart_media.admin
   :members:


Template tags
*************

There is a single template tag you would use in your template on model file fields to
get a proper thumbnail for any supported format.

It uses Sorl library to build the thumbnail but opposed to the Sorl tag,
``media_thumb`` will keep the original format instead of converting it to a normalized
one. This is useful to preserve image when you upload a transparent PNG or an
animated GIF, it won't be converted to a JPEG that would lose alpha channel or
animation and may result to a weird thumbnail.

Also it will allows SVG format but without making a thumbnail since PIL don't support it
and vectorial image can be assumed to fit in any size.

Finally, be aware that you cannot convert Bitmap image to SVG and vice versa, so if you
allow SVG, you need to let the argument ``format`` to ``auto`` value.

.. automodule:: smart_media.templatetags.smart_image
   :members:


Mixin
*****

A mixin object exists to get the right image format name. It is used internally in
template tag but you can also inherit it from a model if you need this format name
somewhere in your code.

.. automodule:: smart_media.mixins
   :members:


SVG
***

To ensure compatibility for both Bitmap and SVG format, we aim to ensure template tag
return can be used in the same way with thumbnail library.

So for a SVG file we return a SvgFile which implement basic attributes and methods
alike Sorl ImageFile.

.. Note::

    Commonly you won't have to deal with it directly so don't bother anymore if you are
    not trying to implement something very specific.

.. automodule:: smart_media.thumbnailing
   :members:


Exceptions
**********

Application parts may raise specific exceptions, it may be helpful to recognize them.

.. automodule:: smart_media.exceptions
   :members:
