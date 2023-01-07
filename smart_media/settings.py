"""
Default application settings
----------------------------

These are the default settings you can override in your own project settings
right after the line which load the default app settings.

"""
SMARTIMAGE_FILESIZE_LIMIT = 5242880
"""
Maximum file size allowed for upload.

This is a limit at Django level so files are still stored until post validation.

You should mind to configure a limit on your webserver to avoid basic attacks
with very big files.

Value could be something like:

* ``5242880`` for ~5MiO;
* ``10485760`` for ~10MiO;
* ``42991616`` for ~50MiO.

See:

https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
"""

SMARTIMAGE_ALLOWED_IMAGE_EXTENSIONS = [
    "jpg",
    "jpeg",
    "svg",
    "gif",
    "png",
]
"""
Allowed image file extensions for image files.

You should accord this list with setting ``SMART_FORMAT_AVAILABLE_FORMATS``.

This is used by ``SmartMediaField`` which includes ``SmartMediaFileExtensionValidator``
that use this setting.

However, you can also use it yourself to your own fields with Django validator
``FileExtensionValidator``: ::

    class MyField(FileField):
        ...
        default_validators = [
            FileExtensionValidator(
                allowed_extensions=settings.SMARTIMAGE_ALLOWED_IMAGE_EXTENSIONS
            ),
        ]

However this won't work with ImageField since allowed extensions contains SVG that is
not a supported image by PIL.

"""

SMART_FORMAT_AVAILABLE_FORMATS = [
    ("jpg", "JPEG"),
    ("jpeg", "JPEG"),
    ("png", "PNG"),
    ("gif", "GIF"),
    ("svg", "SVG"),
]
"""
Available formats for template tag ``media_thumb``.

This is a list of tuples such as ``(extension, name)``, where ``extension`` is
a lowercase file extension (without leading dot) and ``name`` is the format name as
expected from Sorl (excepted for SVG which does not goes through Sorl).

You should accord this list with setting ``SMARTIMAGE_ALLOWED_IMAGE_EXTENSIONS``. All
file fields that are used with template tag ``media_thumb`` must have a format
registered in this setting.
"""
