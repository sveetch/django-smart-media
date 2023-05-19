from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.forms.fields import FileField, ImageField

from .widgets import ClearableFileInputButton


class SmartMediaField(FileField):
    """
    A FileField which define the widget ``ClearableFileInputButton`` and default
    validator ``FileExtensionValidator`` for allowed extensions (as defined from
    setting ``SMARTIMAGE_ALLOWED_IMAGE_EXTENSIONS``).

    .. Note::
        Validation is pretty basic since it works on file extension, no malicious
        Bitmap or SVG image files would be detected here. If it is a concern, you
        will have to develop or use an additional validator.
    """
    widget = ClearableFileInputButton
    default_validators = [
        FileExtensionValidator(
            allowed_extensions=settings.SMARTIMAGE_ALLOWED_IMAGE_EXTENSIONS
        ),
    ]


class SmartImageField(ImageField):
    """
    An ImageField which define the widget ``ClearableFileInputButton``, the default
    validator is still the one from ImageField and so the field won't allow for SVG
    file.
    """
    widget = ClearableFileInputButton
