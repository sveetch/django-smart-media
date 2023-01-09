from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.urls import reverse

from smart_media.modelfields import SmartMediaField
from smart_media.mixins import SmartFormatMixin
from smart_media.utils.file import uploadto_unique
from smart_media.signals import auto_purge_files_on_delete, auto_purge_files_on_change
from smart_media.validators import SmartMediaFileExtensionValidator


def media_uploadto(instance, filename):
    """
    upload_to helper dedicated to field 'media'
    """
    return uploadto_unique("sample/media/%y/%m", instance, filename)


def image_uploadto(instance, filename):
    """
    upload_to helper dedicated to field 'image'
    """
    return uploadto_unique("sample/image/%y/%m", instance, filename)


class ImageItem(SmartFormatMixin, models.Model):
    title = models.CharField(
        "Title",
        blank=False,
        max_length=50,
        default="",
    )

    # Smart model file field with all features included
    cover = SmartMediaField(
        "cover",
        max_length=255,
        null=True,
        blank=True,
        default=None,
        upload_to="sample/cover/%y/%m",
    )

    # A basic FileField with the 'upload_to' helper and file extension validator
    media = models.FileField(
        "media",
        max_length=255,
        null=True,
        blank=True,
        default=None,
        upload_to=media_uploadto,
        validators=[
            SmartMediaFileExtensionValidator(),
        ],
    )

    # A basic ImageField which only use the 'upload_to' helper
    image = models.ImageField(
        "Image",
        max_length=255,
        null=True,
        blank=True,
        default=None,
        upload_to=image_uploadto,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("imageitem-detail", args=[
            str(self.id)
        ])

    # Media format helpers (depends from SmartFormatMixin inheritance)
    def get_media_format(self):
        return self.media_format(self.media)

    def get_image_format(self):
        return self.media_format(self.image)

    class Meta:
        verbose_name = "Image item"
        verbose_name_plural = "Image items"


# Connect signals for automatic file purge
post_delete.connect(
    auto_purge_files_on_delete(["cover", "media", "image"]),
    dispatch_uid="imageitem_files_on_delete",
    sender=ImageItem,
    weak=False,
)

pre_save.connect(
    auto_purge_files_on_change(["cover", "media", "image"]),
    dispatch_uid="imageitem_files_on_change",
    sender=ImageItem,
    weak=False,
)
