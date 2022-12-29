from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.forms.fields import FileField, ImageField

from .widgets import ClearableFileInputButton


class SmartMediaField(FileField):
    widget = ClearableFileInputButton
    default_validators = [
        FileExtensionValidator(
            allowed_extensions=settings.SMARTIMAGE_ALLOWED_IMAGE_EXTENSIONS
        ),
    ]


class SmartImageField(ImageField):
    widget = ClearableFileInputButton
