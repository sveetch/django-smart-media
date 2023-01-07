import pytest

from django.conf import settings
from django.core.exceptions import ValidationError

from smart_media.utils.factories import create_image_file
from smart_media.validators import SmartMediaFileExtensionValidator, validate_file_size


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


def test_extensionvalidator_valid():
    """
    Extension validation should let pass files with proper extensions according to
    settings.
    """
    validator = SmartMediaFileExtensionValidator()

    sample = create_image_file()

    assert validator(sample) is None


def test_extensionvalidator_invalid():
    """
    Extension validation should raise a validation error for files without proper
    extensions.
    """
    validator = SmartMediaFileExtensionValidator()

    sample = create_image_file(filename="foo.zip")

    with pytest.raises(ValidationError) as exc_info:
        validator(sample)

    assert exc_info.value.messages == [
        (
            "File extension “zip” is not allowed. Allowed extensions are: jpg, jpeg, "
            "svg, gif, png."
        ),
    ]
