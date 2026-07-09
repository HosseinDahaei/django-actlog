from __future__ import annotations

import logging

try:
    from celery import shared_task
except ImportError:
    shared_task = None

from actlog.services.logging import _persist_actlog

logger = logging.getLogger(__name__)


if shared_task is not None:

    @shared_task(name="actlog.write_actlog_task", ignore_result=True)
    def write_actlog_task(
        *,
        action: str,
        user_id: int | None = None,
        metadata: dict | None = None,
        ip: str | None = None,
        device_id: str | None = None,
        user_agent: str | None = None,
    ) -> None:
        try:
            _persist_actlog(
                action,
                user_id=user_id,
                metadata=metadata,
                ip=ip,
                device_id=device_id,
                user_agent=user_agent,
            )
        except Exception:
            logger.exception("Failed to persist actlog for action=%s", action)

else:  # pragma: no cover - exercised when celery is not installed
    write_actlog_task = None
