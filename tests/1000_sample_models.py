import pytest

from django.core.exceptions import ValidationError

from smart_media.utils.factories import create_image_file

from sandbox.sample.models import ImageItem
from sandbox.sample.factories import ImageItemFactory


def test_model_basic(db):
    """
    Basic model validation with all required fields should not fail
    """
    imageitem = ImageItem(
        title="Foo",
    )
    imageitem.full_clean()
    imageitem.save()

    url = "/{imageitem_pk}/".format(imageitem_pk=imageitem.id)

    assert 1 == ImageItem.objects.filter(title="Foo").count()
    assert "Foo" == imageitem.title
    assert url == imageitem.get_absolute_url()


def test_model_required_fields(db):
    """
    Basic model validation with missing required files should fail
    """
    imageitem = ImageItem()

    with pytest.raises(ValidationError) as excinfo:
        imageitem.full_clean()

    assert excinfo.value.message_dict == {
        "title": ["This field cannot be blank."],
    }


def test_model_fields_validator(db):
    """
    Extensions validator from 'cover' and 'media' should raise an error for invalid
    file extension.

    'image' field is ignored since this is a ImageField which make validation on image
    validation with PIL instead of file extension.
    """
    sample = create_image_file(filename="foo.zip")

    imageitem = ImageItem(
        title="Foo",
        cover=sample,
        media=sample,
    )
    with pytest.raises(ValidationError) as exc_info:
        imageitem.full_clean()

    assert exc_info.value.message_dict == {
        "cover": [(
            "File extension “zip” is not allowed. Allowed extensions are: jpg, jpeg, "
            "svg, gif, png."
        )],
        "media": [(
            "File extension “zip” is not allowed. Allowed extensions are: jpg, jpeg, "
            "svg, gif, png."
        )],
    }


def test_factory_creation(db):
    """
    Factory should correctly create a new object without any errors
    """
    imageitem = ImageItemFactory(title="foo")
    assert imageitem.title == "foo"
