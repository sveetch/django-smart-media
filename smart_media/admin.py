from django.contrib import admin as django_admin

from .modelfields import SmartMediaField
from .widgets import ClearableFileInputButton


class SmartAdminMixin:
    """
    A class to mix with a Django admin class to the use right widget definition for
    model field ``modelfields.SmartMediaField``.

    .. Note::
        This is required because ModelAdmin translate model fields to widgets using a
        list of harcoded relations between fields and widgets.

        It results in field definitions from ``SmartMediaField.formfield`` to be
        ignored and ``SmartMediaField`` using admin widget ``AdminFileWidget`` instead
        of expected ``ClearableFileInputButton``.

        This mixin will be safe to use with specific model admins that does not allows
        to inherit from ``SmartModelAdmin``.

    Example:

        Your model admin just have to inherit from this class in addition to the model
        admin class: ::

            from django.contrib import admin
            from smart_media.admin import SmartAdminMixin
            from myapp.models import MyModel

            @admin.register(MyModel)
            class MyModelAdmin(SmartAdminMixin, admin.ModelAdmin):
                ...

    If you can't use it, just copy the source of
    ``SmartAdminMixin.formfield_overrides`` (see source) into your own model admin.
    """
    formfield_overrides = {
        SmartMediaField: {
            "widget": ClearableFileInputButton,
        },
    }


class SmartModelAdmin(SmartAdminMixin, django_admin.ModelAdmin):
    """
    A model admin class to include ``SmartAdminMixin``.

    It is only required with model forms in Django admin. If your model admin already
    inherit from a specific admin class, you will prefer to use the
    ``SmartAdminMixin``.

    Example:

        Your model admin just have to inherit from this class: ::

            from django.contrib import admin
            from smart_media.admin import SmartModelAdmin
            from myapp.models import MyModel

            @admin.register(MyModel)
            class MyModelAdmin(SmartModelAdmin):
                ...
    """
    pass
