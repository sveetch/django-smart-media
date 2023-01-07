from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.forms import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _


def validate_file_size(data):
    """
    Validate file size does not exceed limit from
    ``settings.SMARTIMAGE_FILESIZE_LIMIT``.

    Raises:
        ValidationError: If file size is over limit.

    Arguments:
        data (file object):

    Returns:
        boolean: Always True, obvisously excepted if an exception is raised
        when file is over limit.
    """
    msg = _('Please keep file size under {}. Your one was {}')

    if data.size > settings.SMARTIMAGE_FILESIZE_LIMIT:
        raise ValidationError(msg.format(
            filesizeformat(settings.SMARTIMAGE_FILESIZE_LIMIT),
            filesizeformat(data.size)
        ))

    return True


class SmartMediaFileExtensionValidator(FileExtensionValidator):
    """
    TODO
    """
    def __init__(self, *args, **kwargs):
        kwargs["allowed_extensions"] = settings.SMARTIMAGE_ALLOWED_IMAGE_EXTENSIONS

        super().__init__(*args, **kwargs)
