try:
    # Attempt to check for Django>=5.0 behavior
    from django.core.files.storage import storages  # noqa: F401,F403
except ImportError:
    # Fallback to Django<=4.2 behavior
    from django.core.files.storage import get_storage_class
    DEFAULT_STORAGE = get_storage_class()()
else:
    # Result for Django>=5.0
    from django.conf import settings
    from django.utils.module_loading import import_string
    DEFAULT_STORAGE = import_string(settings.STORAGES["default"]["BACKEND"])()


class SvgFile:
    """
    Object to mimic Sorl object ``thumbnail.images.ImageFile`` and implement some of
    its attributes and methods.

    All other method about image size are not supported.

    Attributes:
        name (string): File name, aka its relative path from its storage.
        url (string): Full media file url from its storage.

    Arguments:
        fileobject (django.core.files.File): A valid Django file object.

    Keyword Arguments:
        storage (django.core.files.storage.FileSystemStorage): Storage related
            to the file. If not given, the default Django storage backend is
            used.
    """
    def __init__(self, fileobject, storage=None):
        self.name = fileobject.name
        self.storage = storage or DEFAULT_STORAGE

    def __str__(self):
        return self.name

    def exists(self):
        return self.storage.exists(self.name)

    @property
    def url(self):
        return self.storage.url(self.name)
