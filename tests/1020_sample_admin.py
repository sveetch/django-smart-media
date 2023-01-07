from smart_media.utils.tests import (
    get_admin_add_url, get_admin_change_url, html_pyquery,
)

from sandbox.sample.models import ImageItem
from sandbox.sample.factories import ImageItemFactory


def test_imageitem_admin_add(db, admin_client):
    """
    ImageItem model admin add form view should not raise error on GET request and file
    fields should use the right widget.
    """
    url = get_admin_add_url(ImageItem)
    response = admin_client.get(url)

    assert response.status_code == 200

    dom = html_pyquery(response)

    cover_field = dom.find("#imageitem_form .field-cover .fileinputbutton")
    assert len(cover_field) == 1
    assert cover_field[0].get("class").split() == ["fileinputbutton"]

    media_field = dom.find("#imageitem_form .field-media .fileinputbutton")
    assert len(media_field) == 1
    assert media_field[0].get("class").split() == ["fileinputbutton"]

    image_field = dom.find("#imageitem_form .field-image .fileinputbutton")
    assert len(image_field) == 1
    assert image_field[0].get("class").split() == ["fileinputbutton"]


def test_imageitem_admin_change(db, admin_client):
    """
    ImageItem model admin change view should not raise error on GET request and file
    fields should use the right widget.
    """
    obj = ImageItemFactory()

    url = get_admin_change_url(obj)
    response = admin_client.get(url)

    assert response.status_code == 200

    dom = html_pyquery(response)

    cover_field = dom.find("#imageitem_form .field-cover .fileinputbutton")
    assert len(cover_field) == 1
    assert cover_field[0].get("class").split() == [
        "fileinputbutton", "fileinputbutton--has-preview", "fileinputbutton--clearable",
    ]

    media_field = dom.find("#imageitem_form .field-media .fileinputbutton")
    assert len(media_field) == 1
    assert media_field[0].get("class").split() == [
        "fileinputbutton", "fileinputbutton--has-preview", "fileinputbutton--clearable",
    ]

    image_field = dom.find("#imageitem_form .field-image .fileinputbutton")
    assert len(image_field) == 1
    assert image_field[0].get("class").split() == [
        "fileinputbutton", "fileinputbutton--has-preview", "fileinputbutton--clearable",
    ]
