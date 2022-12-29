from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

from smart_media.mixins import SmartFormatMixin


class ImageItem(SmartFormatMixin, models.Model):
    title = models.CharField(
        "Title",
        blank=False,
        max_length=50,
        default="",
    )

    media = models.FileField(
        "media",
        upload_to="sample/media/%y/%m",
        max_length=255,
        null=True,
        blank=True,
        default=None,
        validators=[
            FileExtensionValidator(
                allowed_extensions=settings.SMARTIMAGE_ALLOWED_IMAGE_EXTENSIONS
            ),
        ],
    )

    image = models.ImageField(
        "Image",
        upload_to="sample/image/%y/%m",
        max_length=255,
        null=True,
        blank=True,
        default=None,
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
