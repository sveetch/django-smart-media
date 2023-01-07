from django.conf import settings

from smart_media.utils.tests import html_pyquery

from sandbox.sample.factories import ImageItemFactory


def test_imageitem_thumbs(db, client):
    """
    Thumb should be correctly created from 'media_thumb' tag usage.
    """
    item = ImageItemFactory()

    response = client.get(item.get_absolute_url())
    assert response.status_code == 200

    # print(decode_response_or_string(response))

    dom = html_pyquery(response)

    cover_link = dom.find("#cover a")[0]
    assert cover_link.get("href").startswith(settings.MEDIA_URL) is True
    assert cover_link.get("href").endswith(".png") is True

    cover_img = cover_link.cssselect("img")[0]
    assert cover_img.get("src") != cover_link.get("href")
    assert cover_img.get("src").startswith(settings.MEDIA_URL) is True
    assert cover_img.get("src").endswith(".png") is True

    media_link = dom.find("#media a")[0]
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
