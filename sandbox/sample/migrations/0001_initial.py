# Generated by Django 4.1.4 on 2023-01-07 15:22

import django.core.validators
from django.db import migrations, models
import sandbox.sample.models
import smart_media.mixins
import smart_media.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ImageItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(default="", max_length=50, verbose_name="Title"),
                ),
                (
                    "cover",
                    smart_media.modelfields.SmartMediaField(
                        blank=True,
                        default=None,
                        max_length=255,
                        null=True,
                        upload_to=sandbox.sample.models.cover_uploadto,
                        verbose_name="cover",
                    ),
                ),
                (
                    "media",
                    models.FileField(
                        blank=True,
                        default=None,
                        max_length=255,
                        null=True,
                        upload_to=sandbox.sample.models.media_uploadto,
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpg", "jpeg", "svg", "gif", "png"]
                            )
                        ],
                        verbose_name="media",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default=None,
                        max_length=255,
                        null=True,
                        upload_to=sandbox.sample.models.image_uploadto,
                        verbose_name="Image",
                    ),
                ),
            ],
            options={
                "verbose_name": "Image item",
                "verbose_name_plural": "Image items",
            },
            bases=(smart_media.mixins.SmartFormatMixin, models.Model),
        ),
    ]
