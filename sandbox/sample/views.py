from django.views.generic import DetailView, FormView

from sandbox.sample.models import ImageItem
from sandbox.sample.forms import ImageItemFieldsForm


class ImageItemDetailView(DetailView):
    """
    A basic detail view, does not make usage of any "smart" feature.
    """
    pk_url_kwarg = "imageitem_pk"
    template_name = "sample/imageitem_detail.html"
    paginate_by = None
    context_object_name = "imageitem_object"
    model = ImageItem


class ImageItemFormView(FormView):
    """
    A basic form view without any model implied.
    """
    form_class = ImageItemFieldsForm
    template_name = "sample/imageitem_form.html"
    success_url = None

    def form_valid(self, form):
        """
        If the form is valid, update attribute did_succeed to True so the template can
        switch from form display to success message.
        """
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        """
        Insert the form into the context dict.
        """
        if "form_did_succeed" not in kwargs:
            kwargs["did_succeed"] = False
        else:
            kwargs["did_succeed"] = True

        return super().get_context_data(**kwargs)
