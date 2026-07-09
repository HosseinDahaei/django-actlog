from django.apps import AppConfig


class ActLogConfig(AppConfig):
    """Configuration for the actlog Django app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "actlog"
    label = "actlog"

    def ready(self) -> None:
        from actlog import receivers  # noqa: F401
