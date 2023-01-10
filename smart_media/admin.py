from django.contrib import admin as django_admin

from .modelfields import SmartMediaField
from .widgets import ClearableFileInputButton


class SmartModelAdmin(django_admin.ModelAdmin):
    """
    Model admin override to include the right widget definition for model field
    ``modelfields.SmartMediaField``.

    This is required because ModelAdmin translate model field to widgets using a list
    of harcoded relations between fields and widgets. It results field definition in
    ``SmartMediaField.formfield`` is ignored and translate ``SmartMediaField`` to
    ``AdminFileWidget`` instead of expected ``ClearableFileInputButton``.

    So either your model admin inherits from ``SmartModelAdmin`` or simply copy its
    ``SmartModelAdmin.formfield_overrides`` into it.

    It is only required with model forms in Django admin.
    """
    formfield_overrides = {
        SmartMediaField: {
            "widget": ClearableFileInputButton,
        },
    }
