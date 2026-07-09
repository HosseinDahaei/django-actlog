"""Default settings and helpers for django-actlog."""

from __future__ import annotations

from typing import Any

from django.apps import apps
from django.conf import settings
from django.db import models

DEFAULTS: dict[str, Any] = {
    "ACTLOG_SYNC": False,
    "ACTLOG_EMIT_IMMEDIATELY": False,
    "ACTLOG_MODEL": "actlog.ActLog",
    "ACTLOG_USER_RELATED_NAME": "act_logs",
    "ACTLOG_ACTION_MAX_LENGTH": 64,
    "ACTLOG_USER_SEARCH_FIELDS": ("user__email",),
    "ACTLOG_CELERY_TASK": None,
}


def get_setting(name: str) -> Any:
    """Return a django-actlog setting, falling back to library defaults."""
    if name in DEFAULTS:
        return getattr(settings, name, DEFAULTS[name])
    return getattr(settings, name)


def get_actlog_model() -> type[models.Model]:
    """Return the configured ActLog model class."""
    model_label = get_setting("ACTLOG_MODEL")
    app_label, model_name = model_label.split(".")
    return apps.get_model(app_label, model_name)
