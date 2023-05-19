from django import forms

from smart_media.widgets import ClearableFileInputButton
from smart_media.fields import SmartMediaField, SmartImageField

from sandbox.sample.models import ImageItem


class ImageItemAdminForm(forms.ModelForm):
    """
    A model form for 'ImageItem', we only need to set proper "smart" widget for
    non-SmartMediaField fields.
    """
    class Meta:
        model = ImageItem
        widgets = {
            "mediafile": ClearableFileInputButton,
            "image": ClearableFileInputButton,
        }
        fields = [
            "title",
            "cover",
            "mediafile",
            "image",
        ]
        exclude = []


class ImageItemFieldsForm(forms.Form):
    """
    A basic form which directly set its form fields.

    This does not implement any data save.
    """
    title = forms.CharField(label="Title", max_length=50, required=True)
    mediafile = SmartMediaField(label="Media", required=False)
    image = SmartImageField(label="Image", required=False)

    def save(self, *args, **kwargs):
        return self.cleaned_data
