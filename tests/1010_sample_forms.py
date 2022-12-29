from django.core.files.uploadedfile import SimpleUploadedFile

from smart_media.utils.tests import DUMMY_GIF_BYTES

from sandbox.sample.factories import ImageItemFactory
from sandbox.sample.forms import ImageItemAdminForm, ImageItemFieldsForm


def test_imageitemadminform_empty():
    """
    Form should not be valid with missing required fields.
    """
    form = ImageItemAdminForm({})

    assert form.is_valid() is False
    assert ("title" in form.errors) is True
    assert len(form.errors) == 1


def test_imageitemadminform_invalid_files(db):
    """
    Form should not be valid when given files are invalid.
    """
    # This already save an ImageItem object but we don't care since there is no
    # uniqueness on this model, and factoryboy build create strategy is more simple to
    # use
    item = ImageItemFactory()

    form = ImageItemAdminForm({
        "title": item.title,
    }, {
        "media": SimpleUploadedFile(
            "small.zip",
            DUMMY_GIF_BYTES,
            content_type="image/gif"
        ),
        "image": "nope",
    })

    assert form.is_valid() is False
    assert ("media" in form.errors) is True
    assert ("image" in form.errors) is True
    assert len(form.errors) == 2


def test_imageitemadminform_success(db):
    """
    Form should be valid with factory datas.
    """
    # This already save an ImageItem object but we don't care since there is no
    # uniqueness on this model, and factoryboy build create strategy is more simple to
    # use
    item = ImageItemFactory()

    form = ImageItemAdminForm({
        "title": item.title,
    }, {
        "media": item.media,
        "image": item.image,
    })

    assert form.is_valid() is True
    assert form.errors.as_data() == {}

    item_instance = form.save()

    assert item_instance.title == item.title
    # Do not check filename itself because it may change once saved on disk
    assert item_instance.media.name.startswith("sample/media/") is True
    assert item_instance.media.name.endswith(".png") is True
    assert item_instance.image.name.startswith("sample/image/") is True
    assert item_instance.image.name.endswith(".png") is True


def test_imageitemfieldsform_empty():
    """
    Form should not be valid with missing required fields.
    """
    form = ImageItemFieldsForm({})

    assert form.is_valid() is False
    assert ("title" in form.errors) is True
    assert len(form.errors) == 1


def test_imageitemfieldsform_success():
    """
    Form should be valid with all required fields and correct submitted data.
    """
    form = ImageItemFieldsForm({
        "title": "foo",
    }, {
        "media": SimpleUploadedFile(
            "media.gif",
            DUMMY_GIF_BYTES,
            content_type="image/gif"
        ),
        "image": SimpleUploadedFile(
            "image.gif",
            DUMMY_GIF_BYTES,
            content_type="image/gif"
        ),
    })

    assert str(form["media"]).startswith('<div class="fileinputbutton">') is True
    assert str(form["image"]).startswith('<div class="fileinputbutton">') is True

    assert form.is_valid() is True
    assert form.errors.as_data() == {}
