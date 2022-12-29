from django import forms

from smart_media.widgets import ClearableFileInputButton
from smart_media.fields import SmartMediaField, SmartImageField

from sandbox.sample.models import ImageItem


class ImageItemAdminForm(forms.ModelForm):
    class Meta:
        model = ImageItem
        widgets = {
            "media": ClearableFileInputButton,
            "image": ClearableFileInputButton,
        }
        fields = [
            "title",
            "media",
            "image",
        ]
        exclude = []


class ImageItemFieldsForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50, required=True)
    media = SmartMediaField(label="Media", required=False)
    image = SmartImageField(label="Image", required=False)

    def save(self, *args, **kwargs):
        return self.cleaned_data
