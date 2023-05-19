from pathlib import Path

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
    Extensions validator from 'cover' and 'mediafile' should raise an error for invalid
    file extension.

    'image' field is ignored since this is a ImageField which make validation on image
    validation with PIL instead of file extension.
    """
    sample = create_image_file(filename="foo.zip")

    imageitem = ImageItem(
        title="Foo",
        cover=sample,
        mediafile=sample,
    )
    with pytest.raises(ValidationError) as exc_info:
        imageitem.full_clean()

    assert exc_info.value.message_dict == {
        "cover": [(
            "File extension “zip” is not allowed. Allowed extensions are: jpg, jpeg, "
            "svg, gif, png."
        )],
        "mediafile": [(
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


def test_article_model_file_purge(db):
    """
    Article 'cover' and 'image' field file should follow correct behaviors:

    * When object is deleted, its files should be delete from filesystem too;
    * When changing file from an object, its previous files (if any) should be
      deleted;
    """
    ping = ImageItemFactory(
        cover=create_image_file(filename="ping_cover_file.png"),
        mediafile=create_image_file(filename="ping_media_file.png"),
        image=create_image_file(filename="ping_image_file.png"),
    )
    pong = ImageItemFactory(
        cover=create_image_file(filename="pong_cover_file.png"),
        mediafile=create_image_file(filename="pong_media_file.png"),
        image=create_image_file(filename="pong_image_file.png"),
    )

    # Memorize some data to use after deletion
    ping_cover_path = ping.cover.path
    ping_media_path = ping.mediafile.path
    ping_image_path = ping.image.path
    pong_cover_path = pong.cover.path
    pong_media_path = pong.mediafile.path
    pong_image_path = pong.image.path

    # Delete object
    ping.delete()

    # Files are deleted along their object
    assert Path(ping_cover_path).exists() is False
    assert Path(ping_media_path).exists() is False
    assert Path(ping_image_path).exists() is False
    # Paranoiac mode: other existing similar filename (as uploaded) are conserved
    # since Django rename file with a unique hash if filename alread exist, they
    # should not be mistaken
    assert Path(pong_cover_path).exists() is True

    # Change object file to a new one
    pong.cover = create_image_file(filename="new_cover.png")
    pong.mediafile = create_image_file(filename="new_media.png")
    pong.image = create_image_file(filename="new_image.png")
    pong.save()

    # During pre save signal, old file is removed from FS and new one is left
    # untouched
    assert Path(pong_cover_path).exists() is False
    assert Path(pong_media_path).exists() is False
    assert Path(pong_image_path).exists() is False
    assert Path(pong.cover.path).exists() is True
    assert Path(pong.mediafile.path).exists() is True
    assert Path(pong.image.path).exists() is True
