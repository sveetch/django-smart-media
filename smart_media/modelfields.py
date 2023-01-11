from django.core.files.utils import validate_file_name
from django.db import models

from .fields import SmartMediaField as SmartMediaFormField
from .utils.file import uploadto_unique
from .validators import SmartMediaFileExtensionValidator


class SmartMediaField(models.FileField):
    """
    A model file field with every "smart" features.

    * Set the ``SmartMediaFileExtensionValidator`` validator;
    * Use the form field ``SmartMediaField`` to get the proper "smart" clearable file
      widget;
    * Generate filename as an unique UUID with ``uploadto_unique`` function;

    Example:

        Usage is identical to a ``models.FileField``: ::

            cover = SmartMediaField(
                "cover",
                max_length=255,
                null=True,
                blank=True,
                default=None,
                upload_to="sample/cover/%y/%m",
            )

    .. Note::

        If attribute ``upload_to`` value is a callable then the UUID filename behavior
        is disabled.

    .. Note::

        Sadly this just won't work on its own in Django admin which makes some internal
        resolutions between model fields and widgets. So you will need to define a rule
        to get the right widget for this field, see
        ``smart_media.admin.SmartModelAdmin``.

    .. Warning::

        Django won't be able to detect change on settings. So you will have to create a
        custom data migration on your own if you want to clean files with previously
        allowed extensions but removed from setting.

    """
    default_validators = [
        SmartMediaFileExtensionValidator(),
    ]

    def generate_filename(self, instance, filename):
        """
        Override ``FileField.generate_filename()`` to change original uploaded filename
        to an UUID.

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
