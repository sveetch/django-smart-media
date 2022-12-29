import pytest

from django.conf import settings
from django.core.exceptions import ValidationError

from smart_media.validators import validate_file_size


class FakeFieldFile:
    """
    Dummy FieldFile to mimic its size attribute without creating a proper FieldFile
    with a real file.
    """
    def __init__(self, size):
        self.size = size


@pytest.mark.parametrize("size, expected", [
    (0, True),
    (1, True),
    (settings.SMARTIMAGE_FILESIZE_LIMIT, True),
])
def test_validate_file_size_valid(size, expected):
    """
    Function should return True for a given FieldFile where file size is not over the
    limit from settings.
    """
    assert validate_file_size(FakeFieldFile(size)) == expected


def test_validate_file_size_invalid():
    """
    Function should raise a ValidationError for a FileField where file size is over the
    limit from settings.
    """
    with pytest.raises(ValidationError):
        validate_file_size(FakeFieldFile(settings.SMARTIMAGE_FILESIZE_LIMIT + 1))
