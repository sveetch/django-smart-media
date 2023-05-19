import factory

from smart_media.utils.factories import create_image_file

from sandbox.sample.models import ImageItem


class ImageItemFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of an ImageItem.
    """
    title = factory.Sequence(lambda n: "Image {0}".format(n))

    class Meta:
        model = ImageItem

    @factory.lazy_attribute
    def cover(self):
        """
        Fill file field with generated image.

        Returns:
            django.core.files.File: File object.
        """

        return create_image_file()

    @factory.lazy_attribute
    def mediafile(self):
        """
        Fill file field with generated image.

        Returns:
            django.core.files.File: File object.
        """

        return create_image_file()

    @factory.lazy_attribute
    def image(self):
        """
        Fill image field with generated image.

        Returns:
            django.core.files.File: File object.
        """

        return create_image_file()
