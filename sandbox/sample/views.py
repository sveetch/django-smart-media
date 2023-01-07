from django.views.generic import DetailView

from sandbox.sample.models import ImageItem


class ImageItemDetailView(DetailView):
    """
    A basic detail view, does not make usage of any "smart" feature.
    """
    pk_url_kwarg = "imageitem_pk"
    template_name = "sample/imageitem_detail.html"
    paginate_by = None
    context_object_name = "imageitem_object"
    model = ImageItem
