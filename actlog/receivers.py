from __future__ import annotations

import importlib
import logging

from django.dispatch import receiver

from actlog.conf import get_setting
from actlog.dispatch import safe_enqueue
from actlog.services.logging import _persist_actlog
from actlog.signals import actlog_event_requested

logger = logging.getLogger(__name__)


def _resolve_celery_task():
    """Return the configured Celery task, or None when Celery is not installed."""
    task_path = get_setting("ACTLOG_CELERY_TASK")
    if task_path:
        module_path, task_name = task_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        return getattr(module, task_name)

    try:
        from actlog.tasks import write_actlog_task
    except ImportError:
        return None
    return write_actlog_task


@receiver(actlog_event_requested)
def enqueue_write_actlog_task(
    *,
    action: str,
    user_id: int | None = None,
    metadata: dict | None = None,
    ip: str | None = None,
    device_id: str | None = None,
    user_agent: str | None = None,
    **_kwargs,
) -> None:
    payload = {
        "action": action,
        "user_id": user_id,
        "metadata": metadata,
        "ip": ip,
        "device_id": device_id,
        "user_agent": user_agent,
    }
    try:
        task = _resolve_celery_task()
        if task is not None:
            safe_enqueue(task, **payload)
        else:
            _persist_actlog(**payload)
    except Exception:
        logger.exception("Failed to process actlog event for action=%s", action)
