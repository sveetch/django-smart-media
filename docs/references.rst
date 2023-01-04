.. _intro_references:

==========
References
==========

This application brings two main features:

* The form parts with fields and widgets to embellish the input and make it more
  ergonomic;
* The template parts with a template tag and model mixin that help to build thumbnails;


Widgets
*******

Base widgets implements the right templates to structure input HTML and the other ones
add stylesheets and Javascript medias to add the input layout. Commonly you will not
use the base ones except in some context where you need to add your stylesheets or
Javascript.

Widgets are the best choice to add Smart Media input since they can work easily on
model forms.

.. automodule:: smart_media.widgets
   :members:


Fields
******

Fields implement widgets for FileField and ImageField but they are less easy to use
with a model form.

.. automodule:: smart_media.fields
   :members:


Template tags
*************

There is a single template tag you would use in your template on model file fields to
get a proper thumbnail for any supported format.

It uses Sorl library to build the thumbnail but opposed to the Sorl tag,
``media_thumb`` will keep the original format instead of converting it to normalized
one. This is useful to preserve image when you upload a transparent PNG or an
animated GIF, it won't be converted to a JPEG that would lose alpha channel or
animation and may result to a weird thumbnail.

Also it will allow SVG format but without making a thumbnail since PIL don't support it
and vectorial image can be assumed to fit in any size.

Finally, be aware that you cannot convert Bitmap image to SVG and vice versa, so if you
allow SVG, you need to let the argument ``format`` to ``auto`` value.

.. automodule:: smart_media.templatetags.smart_image
   :members:


SVG
***

To ensure compatibility for both Bitmap and SVG format, we aim to ensure template tag
return can be used in the same way.

So for SVG file we return a SvgFile which implement basic attributes and methods alike
Sorl ImageFile.

.. automodule:: smart_media.thumbnailing
   :members:


Mixin
*****

A mixin object exists to get the right image format name. It is used internally in
template tag but you can also inherit it from a model if you need this format name
somewhere in your code.

.. automodule:: smart_media.mixins
   :members:

.. automodule:: sandbox.sample.views
   :members:
