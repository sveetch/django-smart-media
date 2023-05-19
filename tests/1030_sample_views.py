from django.conf import settings
from django.urls import reverse

from smart_media.utils.tests import html_pyquery

from sandbox.sample.factories import ImageItemFactory


def test_imageitem_thumbs(db, client):
    """
    Thumb should be correctly created from 'media_thumb' tag usage.
    """
    item = ImageItemFactory()

    response = client.get(item.get_absolute_url())
    assert response.status_code == 200

    dom = html_pyquery(response)

    cover_link = dom.find("#cover a")[0]
    assert cover_link.get("href").startswith(settings.MEDIA_URL) is True
    assert cover_link.get("href").endswith(".png") is True

    cover_img = cover_link.cssselect("img")[0]
    assert cover_img.get("src") != cover_link.get("href")
    assert cover_img.get("src").startswith(settings.MEDIA_URL) is True
    assert cover_img.get("src").endswith(".png") is True

    media_link = dom.find("#mediafile a")[0]
    assert media_link.get("href").startswith(settings.MEDIA_URL) is True
    assert media_link.get("href").endswith(".png") is True

    media_img = media_link.cssselect("img")[0]
    assert media_img.get("src") != media_link.get("href")
    assert media_img.get("src").startswith(settings.MEDIA_URL) is True
    assert media_img.get("src").endswith(".png") is True

    image_link = dom.find("#image a")[0]
    assert image_link.get("href").startswith(settings.MEDIA_URL) is True
    assert image_link.get("href").endswith(".png") is True

    image_img = image_link.cssselect("img")[0]
    assert image_img.get("src") != image_link.get("href")
    assert image_img.get("src").startswith(settings.MEDIA_URL) is True
    assert image_img.get("src").endswith(".png") is True


def test_imageitem_form(db, client):
    """
    View should displays form with expted HTML fields and form media assets.
    """
    urlname = "sample:imageitem-form"
    response = client.get(reverse(urlname))
    assert response.status_code == 200

    # from smart_media.utils.tests import decode_response_or_string
    # print(decode_response_or_string(response))

    dom = html_pyquery(response)

    media_field = dom.find("#mediafile .fileinputbutton")
    assert len(media_field) == 1
    assert media_field[0].get("class").split() == ["fileinputbutton"]

    image_field = dom.find("#image .fileinputbutton")
    assert len(image_field) == 1
    assert image_field[0].get("class").split() == ["fileinputbutton"]

    ressource_links = dom.find("link")
    assert "/static/smart_image/css/fileinputbutton.css" in (
        [item.get("href") for item in ressource_links]
    )

    ressource_scripts = dom.find("script")
    assert "/static/smart_image/js/fileinputbutton.js" in (
        [item.get("src") for item in ressource_scripts]
    )
