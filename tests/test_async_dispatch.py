from unittest import mock

import pytest
from actlog.dispatch import emit_on_commit, safe_enqueue
from django.db import transaction
from django.dispatch import Signal

try:
    from kombu.exceptions import OperationalError
except ImportError:
    OperationalError = type("OperationalError", (Exception,), {})  # type: ignore[misc]


@pytest.mark.django_db
def test_safe_enqueue_runs_inline_when_broker_unavailable(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = False
    task = mock.Mock()
    task.name = "actlog.write_actlog_task"
    task.delay.side_effect = OperationalError("connection refused")
    task.apply.return_value = None

    safe_enqueue(task, foo="bar")

    task.delay.assert_called_once_with(foo="bar")
    task.apply.assert_called_once_with(kwargs={"foo": "bar"})


@pytest.mark.django_db
def test_safe_enqueue_uses_apply_when_celery_eager(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    task = mock.Mock()
    task.name = "actlog.write_actlog_task"

    safe_enqueue(task, foo="bar")

    task.delay.assert_not_called()
    task.apply.assert_called_once_with(kwargs={"foo": "bar"})


@pytest.mark.django_db
def test_safe_enqueue_swallows_eager_task_failure(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    task = mock.Mock()
    task.name = "actlog.write_actlog_task"
    task.apply.side_effect = RuntimeError("provider unavailable")

    safe_enqueue(task, foo="bar")

    task.delay.assert_not_called()
    task.apply.assert_called_once_with(kwargs={"foo": "bar"})


@pytest.mark.django_db(transaction=True)
def test_emit_on_commit_defers_until_commit(settings):
    settings.ACTLOG_EMIT_IMMEDIATELY = False
    signal = Signal()
    handler = mock.Mock()
    signal.connect(handler)

    with transaction.atomic():
        emit_on_commit(signal, action="TEST")
        handler.assert_not_called()

    handler.assert_called_once()


@pytest.mark.django_db
def test_emit_on_commit_sends_immediately_when_configured(settings):
    settings.ACTLOG_EMIT_IMMEDIATELY = True
    signal = Signal()
    handler = mock.Mock()
    signal.connect(handler)

    emit_on_commit(signal, action="TEST")

    handler.assert_called_once()
