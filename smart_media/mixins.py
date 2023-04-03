from django.conf import settings


class SmartFormatMixin:
    """
    A mixin to inherit from a model so it will have a helper method to manage image
    formats.

    Example:

        You just have to inherit this class then define a method dedicated to your
        field: ::

            from django.db import models
            from smart_media.mixins import SmartFormatMixin
            from smart_media.modelfields import SmartMediaField

            class MyModel(SmartFormatMixin, models.Model):
                media = SmartMediaField(
                    "media",
                    max_length=255,
                    null=True,
                    blank=True,
                    default=None,
                    upload_to="sample/media/%y/%m",
                )

                def get_media_format(self):
                    return self.media_format(self.media)
    """

    def media_format(self, mediafile):
        """
        Common method to perform a naive check about image format using file
        extension.

        Retrieved format will come from setting ``SMART_FORMAT_AVAILABLE_FORMATS``.

        Obviously since it use the file extension, found format is not to be
        100% trusted. You may think about validate your files strictly if strong
        security is a matter for you and file upload is open to untrusted user.

        Arguments:
            mediafile (object): Either a FileField, ImageField or any other
                object which implement a ``name`` attribute which return the
                filename.

        Return:
            string: Format name if filename extension match to any available
            format extension from available formats else it returns ``None``.
        """
        if mediafile:
            ext = mediafile.name.split(".")[-1].lower()

            for fileext, formatname in settings.SMART_FORMAT_AVAILABLE_FORMATS:
                if ext == fileext:
                    return formatname

        return None
