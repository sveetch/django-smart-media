from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

from smart_media.modelfields import SmartMediaField
from smart_media.mixins import SmartFormatMixin
from smart_media.utils.file import uploadto_unique


#def cover_uploadto(instance, filename):
    #return uploadto_unique("sample/cover/%y/%m", instance, filename)


def media_uploadto(instance, filename):
    return uploadto_unique("sample/media/%y/%m", instance, filename)


def image_uploadto(instance, filename):
    return uploadto_unique("sample/image/%y/%m", instance, filename)


class ImageItem(SmartFormatMixin, models.Model):
    title = models.CharField(
        "Title",
        blank=False,
        max_length=50,
        default="",
    )

    cover = SmartMediaField(
        "cover",
        max_length=255,
        null=True,
        blank=True,
        default=None,
        upload_to="sample/cover/%y/%m",
    )

    media = models.FileField(
        "media",
        max_length=255,
        null=True,
        blank=True,
        default=None,
        upload_to=media_uploadto,
        validators=[
            FileExtensionValidator(
                allowed_extensions=settings.SMARTIMAGE_ALLOWED_IMAGE_EXTENSIONS
            ),
        ],
    )

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
        """
        Return absolute URL to the blog detail view.

        Returns:
            string: An URL.
        """
        return reverse("imageitem-detail", args=[
            str(self.id)
        ])

    def get_media_format(self):
        return self.media_format(self.media)

    def get_image_format(self):
        return self.media_format(self.image)

    class Meta:
        verbose_name = "Image item"
        verbose_name_plural = "Image items"
