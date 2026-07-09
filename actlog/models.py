"""ActLog model for explicit application event logging."""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone

from actlog.conf import get_setting


class ActLog(models.Model):
    """Immutable application event record."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name=get_setting("ACTLOG_USER_RELATED_NAME"),
    )
    action = models.CharField(
        max_length=get_setting("ACTLOG_ACTION_MAX_LENGTH"),
        db_index=True,
    )
    ip = models.GenericIPAddressField(null=True, blank=True)
    device_id = models.CharField(max_length=255, blank=True, default="")
    user_agent = models.TextField(blank=True, default="")
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        db_index=True,
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["action", "-created_at"],
                name="actlog_action_created_idx",
            ),
            models.Index(
                fields=["user", "-created_at"],
                name="actlog_user_created_idx",
            ),
        ]
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"action={self.action} user={self.user_id} at={self.created_at.isoformat()}"
