"""Audit logging service entrypoint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from actlog.choices import Level
from actlog.conf import get_actlog_model

if TYPE_CHECKING:
    from actlog.models import ActLog


def _persist_actlog(
    action: str,
    *,
    user_id: int | None = None,
    metadata: dict | None = None,
    level: str | None = None,
) -> ActLog:
    model = get_actlog_model()
    if level is None:
        level = Level.INFO
    return model.objects.create(
        user_id=user_id,
        action=action,
        level=level,
        metadata=dict(metadata or {}),
    )


def log_event(
    action: str,
    *,
    user=None,
    metadata: dict | None = None,
    level: str | None = None,
) -> ActLog:
    """Persist an application event synchronously and return the created ActLog."""
    user_id = user.id if user is not None else None
    return _persist_actlog(
        action,
        user_id=user_id,
        metadata=metadata,
        level=level,
    )
