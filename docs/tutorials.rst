.. _Sorl: https://github.com/jazzband/sorl-thumbnail

.. _tutorial_intro:

=========
Tutorials
=========

Here you will find common implementations that may fit to your project cases.


Add 'SmartMediaField' to a simple form without a model
******************************************************

This is simple since no model or admin is involved.

Here is a form example: ::

    from django import forms

    from smart_media.fields import SmartMediaField


    class BasicForm(forms.Form):
        """
        A basic form which directly set its form fields.
        """
        mediafile = SmartMediaField(label="Media", required=False)

Obviously, since it is a non model form, you will have to manage data save yourself and
especially the upload file save.

Add 'SmartMediaField' to a model
********************************

For the following model: ::

    from django.db import models
    from django.db.models.signals import post_delete, pre_save
    from django.urls import reverse

    from smart_media.modelfields import SmartMediaField
    from smart_media.mixins import SmartFormatMixin
    from smart_media.signals import auto_purge_files_on_delete, auto_purge_files_on_change


    class MediaItem(SmartFormatMixin, models.Model):
        title = models.CharField(
            "title",
            blank=False,
            max_length=50,
            default="",
        )

        mediafile = SmartMediaField(
            "media",
            max_length=255,
            null=True,
            blank=True,
            default=None,
            upload_to="sample/mediafile/%y/%m",
        )

        def __str__(self):
            return self.title

        def get_absolute_url(self):
            return reverse("sample:mediaitem-detail", args=[str(self.id)])

        def get_media_format(self):
            """
            Media format helper return the format name for file from 'MediaItem.mediafile'
            value.
            """
            return self.media_format(self.mediafile)

        class Meta:
            verbose_name = "Media item"
            verbose_name_plural = "Media items"


    # Connect signals for automatic file purge
    post_delete.connect(
        auto_purge_files_on_delete(["mediafile"]),
        dispatch_uid="mediaitem_files_on_delete",
        sender=MediaItem,
        weak=False,
    )

    pre_save.connect(
        auto_purge_files_on_change(["mediafile"]),
        dispatch_uid="mediaitem_files_on_change",
        sender=MediaItem,
        weak=False,
    )

Explanations:

* ``SmartFormatMixin`` is a base class to inherit from to implement media format helper,
  this optional if you don't want to implement ``MediaItem.get_media_format`` method;
* ``title`` field is just a basic text field for the example;
* ``SmartMediaField`` is used for the mediafile field, it implements every features;
* ``MediaItem.get_media_format`` is just a helper to get the media format name, this
  may be useful in templates to make conditions on some specific formats;
* ``post_delete`` and ``pre_save`` signals are connected to ``MediaItem.mediafile``
  field to automatically purge its stale file when updated to a new one (or emptied);

And finally we will need a custom admin to enable SmartMedia features: ::

    from django.contrib import admin

    from smart_media.admin import SmartModelAdmin

    from sandbox.sample.models import MediaItem


    @admin.register(MediaItem)
    class MediaItemAdmin(SmartModelAdmin):
        """
        Admin view for 'MediaItem'
        """
        pass

We need this model admin to patch a Django behavior that would lead to a basic
``FileField`` without SmartMedia features since by default the admin would translate it
to an internal admin field.

.. Note::
    ``SmartModelAdmin`` is just a subclass of ``django.contrib.admin.ModelAdmin`` to
    define ``formfield_overrides`` rule for ``SmartMediaField``.

    If you need to subclass another ``ModelAdmin`` class, just use it and inherits also
    from ``smart_media.admin.SmartAdminMixin`` instead ``SmartModelAdmin``.

    Or even just define the ``formfield_overrides`` yourself within your model admin.
