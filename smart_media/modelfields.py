from django.conf import settings
from django.core.files.utils import validate_file_name
from django.db import models

from .fields import SmartMediaField as SmartMediaFormField
from .utils.file import uploadto_unique
from .validators import SmartMediaFileExtensionValidator


class SmartMediaField(models.FileField):
    """
    A model file field with every "smart" features.

    * Set the ``SmartMediaFileExtensionValidator`` validator;
    * Use the form field ``SmartMediaField``;
    * Generate filename as an unique UUID with ``uploadto_unique`` function;

    Usage is identical to the ``models.FileField``: ::

        cover = SmartMediaField(
            "cover",
            max_length=255,
            null=True,
            blank=True,
            default=None,
            upload_to="sample/cover/%y/%m",
        )

    .. Note::

        If 'upload_to' is a callable the UUID behavior is disabled.

    .. Note::

        Django won't be able to detect change on settings. So you will have to create a
        custom data migration on your own if you want to clean files with previously
        allowed extensions but removed from setting.

    """
    default_validators = [
        SmartMediaFileExtensionValidator(),
    ]

    def generate_filename(self, instance, filename):
        """
        Override default FileField method to use UUID for filename.

        'upload_to' date pattern is still properly formatted and the UUID behavior is
        ignored if 'upload_to' is a callable.
        """
        if callable(self.upload_to):
            filename = self.upload_to(instance, filename)
        else:
            filename = uploadto_unique(str(self.upload_to), instance, filename)

        filename = validate_file_name(filename, allow_relative_path=True)

        return self.storage.generate_filename(filename)

    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "form_class": SmartMediaFormField,
                **kwargs,
            }
        )