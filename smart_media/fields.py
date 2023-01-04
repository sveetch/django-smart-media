from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.forms.fields import FileField, ImageField

from .widgets import ClearableFileInputButton


class SmartMediaField(FileField):
    """
    A FileField which define the widget ``ClearableFileInputButton`` and default
    validator ``FileExtensionValidator`` for allowed extensions (as defined from
    setting ``SMARTIMAGE_ALLOWED_IMAGE_EXTENSIONS``).
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
