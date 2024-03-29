import pytest

from smart_media.mixins import SmartFormatMixin


class DummyFile:
    """
    Dummy File object just for ``name`` attribute.
    """
    def __init__(self, name):
        self.name = name


@pytest.mark.parametrize("filename,expected", [
    (
        None,
        None,
    ),
    (
        "bar",
        None,
    ),
    (
        "bar.txt",
        None,
    ),
    (
        "bar.jp.txt",
        None,
    ),
    (
        "bar.jpg",
        "JPEG",
    ),
    (
        "bar.jpeg",
        "JPEG",
    ),
    (
        "bar.txt.jpg",
        "JPEG",
    ),
    (
        "bar.png",
        "PNG",
    ),
    (
        "bar.gif",
        "GIF",
    ),
    (
        "bar.svg",
        "SVG",
    ),
])
def test_validate_file_size_success_under(filename, expected):
    """
    media_format method should return the right format name according to file
    extension.
    """
    mixin = SmartFormatMixin()

    dummy = DummyFile(filename) if filename else None

    assert expected == mixin.media_format(dummy)
