from ..settings import (
    SMARTIMAGE_FILESIZE_LIMIT,
    SMARTIMAGE_ALLOWED_IMAGE_EXTENSIONS,
    SMART_FORMAT_AVAILABLE_FORMATS,
)


class SmartMediaDefaultSettings:
    """
    Default "Django smart media" settings class to use with a "django-configuration"
    class.

    Example:

        You could use it like so: ::

            from configurations import Configuration
            from smart_media.contrib.django_configuration import (
                SmartMediaDefaultSettings,
            )

            class Dev(SmartMediaDefaultSettings, Configuration):
                DEBUG = True

                SMARTIMAGE_FILESIZE_LIMIT = 142

        This will override only the setting ``SMARTIMAGE_FILESIZE_LIMIT``, all other
        SmartMedia settings will have the default values from ``smart_media.settings``.
    """

    SMARTIMAGE_FILESIZE_LIMIT = SMARTIMAGE_FILESIZE_LIMIT

    SMARTIMAGE_ALLOWED_IMAGE_EXTENSIONS = SMARTIMAGE_ALLOWED_IMAGE_EXTENSIONS

    SMART_FORMAT_AVAILABLE_FORMATS = SMART_FORMAT_AVAILABLE_FORMATS
