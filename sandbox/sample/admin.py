from django.contrib import admin

from sandbox.sample.models import ImageItem
from sandbox.sample.forms import ImageItemAdminForm


@admin.register(ImageItem)
class ImageItemAdmin(admin.ModelAdmin):
    """
    Admin view for 'ImageItem', we need to set the model form where we define the
    proper widgets.
    """
    form = ImageItemAdminForm
