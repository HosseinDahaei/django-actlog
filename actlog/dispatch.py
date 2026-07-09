"""Helpers for deferring side effects until after commit and enqueueing Celery tasks."""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from django.db import transaction
from django.dispatch import Signal

from actlog.conf import get_setting

logger = logging.getLogger(__name__)

try:
    from kombu.exceptions import OperationalError
except ImportError:  # pragma: no cover - kombu ships with celery
    OperationalError = ()  # type: ignore[misc, assignment]

_BROKER_UNAVAILABLE_ERRORS: tuple[type[BaseException], ...] = (
    OperationalError,
    ConnectionError,
    ConnectionRefusedError,
    OSError,
)


def emit_on_commit(signal: Signal, /, *, sender: Any | None = None, **kwargs: Any) -> None:
    """Send a signal only after the current transaction commits."""
    resolved_sender = signal if sender is None else sender

    def _send() -> None:
        signal.send(sender=resolved_sender, **kwargs)

    if get_setting("ACTLOG_EMIT_IMMEDIATELY"):
        _send()
        return

    transaction.on_commit(_send)


def _is_broker_unavailable(exc: BaseException) -> bool:
    if isinstance(exc, _BROKER_UNAVAILABLE_ERRORS):
        return True
    cause = exc.__cause__
    return cause is not None and _is_broker_unavailable(cause)


def _run_task_inline(task: Callable[..., Any], /, **kwargs: Any) -> None:
    task.apply(kwargs=kwargs)


def safe_enqueue(task: Callable[..., Any], /, **kwargs: Any) -> None:
    """Enqueue a Celery task; run inline when eager or the broker is down."""
    from django.conf import settings

    if getattr(settings, "CELERY_TASK_ALWAYS_EAGER", False):
        try:
            _run_task_inline(task, **kwargs)
        except Exception:
            logger.exception("Failed to run eager task %s", getattr(task, "name", task))
        return

    try:
        task.delay(**kwargs)
    except Exception as exc:
        if not _is_broker_unavailable(exc):
            logger.exception("Failed to enqueue task %s", getattr(task, "name", task))
            return
        logger.warning(
            "Broker unavailable, running task %s inline",
            getattr(task, "name", task),
        )
        try:
            _run_task_inline(task, **kwargs)
        except Exception:
            logger.exception("Failed to run task %s inline", getattr(task, "name", task))
