from pathlib import Path

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

from smart_media.thumbnailing import SvgFile
from smart_media.utils.tests import get_test_source


def test_svgfile():
    """
    SvgFile should have "name" attribute, "url" attribute correct values and
    "exists" method correct response.
    """
    # Create a dummy source image file
    image = get_test_source(DEFAULT_STORAGE, format_name="SVG")
    saved_source = DEFAULT_STORAGE.path(image.name)

    assert Path(saved_source).exists()

    svg = SvgFile(image)

    assert svg.name == image.name
    assert svg.exists() is True

    # Ensure url starts like a url and ends with the file name without to test
    # the full url matching
    assert len(svg.url) > 0
    assert svg.url.startswith("/")
    assert svg.url.endswith(image.name)
