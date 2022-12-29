from django.conf import settings


class SmartFormatMixin:
    """
    A mixin to inherit from a model so it will have a helper method to manage image
    formats.
    """

    def media_format(self, mediafile):
        """
        Common method to perform a naive check about image format using file
        extension.

        This has been done for common image formats, so it will return either
        'JPEG', 'PNG', 'SVG' or None if it does not match any of these formats.

        Obviously, since it use the file extension, found format is not to be
        100% trusted. For sanity, media saving should validate it correctly
        and possibly enforce the right file extension according to file format
        found from file metas (like with the PIL method to get it).

        At least the FileField should validate uploaded file is a valid image (except
        for SVG). This method won't perform stronger validation since it may be widely
        used in code and template and we don't want to open file again and again.

        Arguments:
            mediafile (object): Either a FileField, ImageField or any other
                object which implement a ``name`` attribute which return the
                filename.

        Return:
            string: Format name if filename extension match to any available
            format extension, else ``None``.
        """
        if mediafile:
            ext = mediafile.name.split(".")[-1].lower()

            for fileext, formatname in settings.SMART_FORMAT_AVAILABLE_FORMATS:
                if ext == fileext:
                    return formatname

        return None
