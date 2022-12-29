from pathlib import Path

from django.core.files.storage import get_storage_class

from smart_media.thumbnailing import SvgFile
from smart_media.utils.tests import get_test_source


def test_svgfile():
    """
    SvgFile should have "name" attribute, "url" attribute correct values and
    "exists" method correct response.
    """
    storage = get_storage_class()()

    # Create a dummy source image file
    image = get_test_source(
        storage,
        format_name="SVG",
    )
    saved_source = storage.path(image.name)

    assert Path(saved_source).exists()

    svg = SvgFile(image)

    assert svg.name == image.name
    assert svg.exists() is True

    # Ensure url starts like a url and ends with the file name without to test
    # the full url matching
    assert len(svg.url) > 0
    assert svg.url.startswith("/")
    assert svg.url.endswith(image.name)
