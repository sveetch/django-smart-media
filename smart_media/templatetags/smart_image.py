from django import template
from django.conf import settings

from sorl.thumbnail.shortcuts import get_thumbnail

from ..exceptions import (
    InvalidFormatError, IncompatibleSvgToBitmap, IncompatibleBitmapToSvg
)
from ..mixins import SmartFormatMixin
from ..thumbnailing import SvgFile

register = template.Library()


@register.simple_tag
def media_thumb(source, geometry, *args, **kwargs):
    """

    Determine the right format and return the Sorl thumb file url path for
    given image file.

    .. _Sorl: https://github.com/jazzband/sorl-thumbnail

    Arguments:
        source (object): Either a FileField or an ImageField.
        geometry (string): Geometry string as expected by Sorl. It should be
            something like ``200`` for 200px width and automatic height or
            ``200x100`` for 200px width and 100px height.
        *args: Not used, there is no other expected positionnal arguments.
        **kwargs: Keyword arguments are passed to `Sorl`_, watch its documentation
            for more details.

    Keyword Arguments:
        format (string):
            An available format name from settings ``SMART_FORMAT_AVAILABLE_FORMATS``:

            * ``PNG``, ``JPEG`` and ``GIF`` enforce the thumb format no matter
              the source image format. Be careful to not enforce a format where
              a SVG is a possible source format, since Sorl can't read SVG.
            * ``SVG`` will not produce any thumb, just return the same path
              than the source one since SVG does not need a thumb and is not
              supported from image libraries.
            * ``auto`` to automatically find and use the same format than
              the source image. This is the recommended way.

            When argument is empty the default value is ``auto``.

    Example:
        The most basic usage is to define only thumbnail geometry in default
        "auto" format mode: ::

            {% load smart_image %}
            {% media_thumb instance.image "250x200" as thumb %}
            <img src="{{ thumb.url }}" alt="">

        You can also enforce a specific format: ::

            {% load smart_image %}
            {% media_thumb instance.image "250x200" format="JPEG" as thumb %}
            <img src="{{ thumb.url }}" alt="">

        Keep it in mind this will raise an error with SVG image files (if you
        allowed SVG format in plugins) since image libraries (like Pillow or
        ImageMagick) has no support for SVG.

        Every argument but ``format`` is passed to Sorl, so for cropping an image you
        can do : ::

            {% load smart_image %}
            {% media_thumb instance.image "250x200" crop="center" as thumb %}
            <img src="{{ thumb.url }}" alt="">

        Again, see `Sorl`_ documentation to know about available options.

    Return:
        sorl.thumbnail.images.ImageFile or SvgFile: Either Sorl ImageFile instance for
        created thumb or SvgFile which mimic Sorl ImageFile.
    """
    # Safe return when there is no source file
    # NOTE: Should trigger a warning log ?
    if not source:
        return None

    required_format = kwargs.pop("format", "auto")
    source_extension = source.name.split(".")[-1].lower()

    available_extensions = [k for k, v in settings.SMART_FORMAT_AVAILABLE_FORMATS]

    # Automatic format guess
    if required_format.lower() == "auto":
        required_format = SmartFormatMixin().media_format(source)
    # Specific SVG format
    elif required_format.lower() == "svg":
        # A bitmap file cannot be converted to a SVG
        if source_extension != "svg":
            msg = ("Incompatible required format (SVG) with source format "
                   "(Bitmap).")
            raise IncompatibleBitmapToSvg(msg.format(
                format_name=required_format.lower(),
            ))
        # SVG to SVG is correct (nothing to do)
        return SvgFile(source)
    # Unknown format
    elif required_format.lower() not in available_extensions:
        msg = ("Required format '{format_name}' does not match available "
               "formats: {available}")
        raise InvalidFormatError(msg.format(
            format_name=required_format.lower(),
            available=", ".join(available_extensions),
        ))
    # SVG source with required bitmap format
    elif source_extension == "svg":
        msg = ("Incompatible required format (Bitmap) with source format "
               "(SVG).")
        raise IncompatibleSvgToBitmap(msg.format(
            format_name=required_format.lower(),
        ))

    kwargs["format"] = required_format

    # Vector format does not create a thumb and so just return original
    # source file
    if required_format == "SVG":
        return SvgFile(source)

    # Here we assume the format is ok, if it has been manually defined, user
    # is responsible about possible error with its content
    return get_thumbnail(source, geometry, **kwargs)
