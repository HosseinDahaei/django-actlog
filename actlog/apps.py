from django.apps import AppConfig
from django.conf import settings

DJANGO_JSON_WIDGET_APP = "django_json_widget"

if settings.configured and DJANGO_JSON_WIDGET_APP not in settings.INSTALLED_APPS:
    settings.INSTALLED_APPS.append(DJANGO_JSON_WIDGET_APP)


class ActLogConfig(AppConfig):
    """Configuration for the actlog Django app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "actlog"
    label = "actlog"
