from django.contrib import admin

from smart_media.admin import SmartModelAdmin

from sandbox.sample.forms import ImageItemAdminForm
from sandbox.sample.models import ImageItem


@admin.register(ImageItem)
class ImageItemAdmin(SmartModelAdmin):
    """
    Admin view for 'ImageItem', we need to set the model form where we define the
    proper widgets.
    """
    form = ImageItemAdminForm
