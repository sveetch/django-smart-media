from django.contrib import admin as django_admin

from .modelfields import SmartMediaField
from .widgets import ClearableFileInputButton


class SmartModelAdmin(django_admin.ModelAdmin):
    """
    A model admin class to include the right widget definition for model field
    ``modelfields.SmartMediaField``.

    This is required because ModelAdmin translate model field to widgets using a list
    of harcoded relations between fields and widgets. It results field definition in
    ``SmartMediaField.formfield`` is ignored and translate ``SmartMediaField`` to
    ``AdminFileWidget`` instead of expected ``ClearableFileInputButton``.

    So either your model admin inherits from ``SmartModelAdmin`` or simply copy its
    ``SmartModelAdmin.formfield_overrides`` into it.

    It is only required with model forms in Django admin.

    Example:

        Your model admin just have to inherit from this class: ::

            from django.contrib import admin
            from smart_media.admin import SmartModelAdmin
            from myapp.models import MyModel

            @admin.register(MyModel)
            class MyModelAdmin(SmartModelAdmin):
                ...

    Or copy the source of ``SmartModelAdmin.formfield_overrides`` (see source) into
    your own model admin.
    """
    formfield_overrides = {
        SmartMediaField: {
            "widget": ClearableFileInputButton,
        },
    }
