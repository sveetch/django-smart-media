from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class smart_mediaConfig(AppConfig):
    name = "smart_media"
    verbose_name = _("Django smart image")
    default_auto_field = "django.db.models.AutoField"
