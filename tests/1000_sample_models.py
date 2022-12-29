import pytest

from django.core.exceptions import ValidationError

from sandbox.sample.models import ImageItem
from sandbox.sample.factories import ImageItemFactory


def test_basic(db):
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


def test_required_fields(db):
    """
    Basic model validation with missing required files should fail
    """
    imageitem = ImageItem()

    with pytest.raises(ValidationError) as excinfo:
        imageitem.full_clean()

    assert excinfo.value.message_dict == {
        "title": ["This field cannot be blank."],
    }


def test_creation(db):
    """
    Factory should correctly create a new object without any errors
    """
    imageitem = ImageItemFactory(title="foo")
    assert imageitem.title == "foo"
