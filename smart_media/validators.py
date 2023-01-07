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
    Customized ``FileExtensionValidator`` to directly get the allowed extension from
    setting ``SMARTIMAGE_ALLOWED_IMAGE_EXTENSIONS``.

    Since allowed extensions are embedded in code from settings, Django won't detect
    any change model change when changing the setting and so won't create a migration.

    Argument ``allowed_extensions`` is still accepted but is ignored.
    """
    def __init__(self, *args, **kwargs):
        kwargs["allowed_extensions"] = settings.SMARTIMAGE_ALLOWED_IMAGE_EXTENSIONS

        super().__init__(*args, **kwargs)
