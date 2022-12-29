from django.core.files.storage import get_storage_class


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
        self.storage = storage or get_storage_class()()

    def __str__(self):
        return self.name

    def exists(self):
        return self.storage.exists(self.name)

    @property
    def url(self):
        return self.storage.url(self.name)
