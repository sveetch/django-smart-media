from django.contrib import admin

from sandbox.sample.models import ImageItem
from sandbox.sample.forms import ImageItemAdminForm


@admin.register(ImageItem)
class ImageItemAdmin(admin.ModelAdmin):
    form = ImageItemAdminForm
