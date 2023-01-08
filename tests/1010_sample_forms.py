from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile

from smart_media.utils.tests import DUMMY_GIF_BYTES
from smart_media.utils.factories import create_image_file

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
    # uniqueness on this model, and factoryboy create strategy is more simple to
    # use with files than the build one.
    item = ImageItemFactory()

    form = ImageItemAdminForm({
        "title": item.title,
    }, {
        "cover": SimpleUploadedFile(
            "small.zip",
            DUMMY_GIF_BYTES,
            content_type="image/gif"
        ),
        "media": SimpleUploadedFile(
            "small.zip",
            DUMMY_GIF_BYTES,
            content_type="image/gif"
        ),
        "image": "nope",
    })

    assert str(form["cover"]).startswith('<div class="fileinputbutton">') is True
    assert str(form["media"]).startswith('<div class="fileinputbutton">') is True
    assert str(form["image"]).startswith('<div class="fileinputbutton">') is True

    assert form.is_valid() is False
    assert ("cover" in form.errors) is True
    assert ("media" in form.errors) is True
    assert ("image" in form.errors) is True
    assert len(form.errors) == 3


def test_imageitemadminform_success(db):
    """
    Form should be valid with factory datas.

    Also we ensure file are correctly saved.
    """
    # Build file apart to use custom filename and keep reference to original filename
    # that would be lost from factory returns
    cover_file = create_image_file(filename="cover_file.png")
    media_file = create_image_file(filename="media_file.png")
    image_file = create_image_file(filename="image_file.png")

    # This already save an ImageItem object but we don't care since there is no
    # uniqueness on this model and factoryboy build create strategy is simpler to use
    item = ImageItemFactory(
        cover=cover_file,
        media=media_file,
        image=image_file,
    )

    form = ImageItemAdminForm({
        "title": item.title,
    }, {
        "cover": item.cover,
        "media": item.media,
        "image": item.image,
    })

    is_valid = form.is_valid()
    # print(form.errors.as_data())
    assert is_valid is True
    assert form.errors.as_data() == {}

    item_instance = form.save()

    # SmartMediaField directly include the UUID filename on upload_to
    cover_filename = Path(item_instance.cover.name).name
    assert item_instance.cover.name.startswith("sample/cover/") is True
    assert cover_filename.startswith("cover_file") is False
    assert cover_filename.endswith(".png") is True

    # 'media' FileField set the 'upload_to' helper for UUID filename
    media_filename = Path(item_instance.media.name).name
    assert item_instance.media.name.startswith("sample/media/") is True
    assert media_filename.startswith("media_file") is False
    assert media_filename.endswith(".png") is True

    # 'image' FileField set the 'upload_to' helper for UUID filename
    image_filename = Path(item_instance.image.name).name
    assert item_instance.image.name.startswith("sample/image/") is True
    assert image_filename.startswith("image_file") is False
    assert image_filename.endswith(".png") is True


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
