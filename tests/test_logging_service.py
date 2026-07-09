import pytest
from actlog.models import ActLog
from actlog.services.logging import log_event
from django.contrib.auth import get_user_model
from django.test import RequestFactory

TEST_ACTION = "TEST_ACTION"


def test_log_event_extracts_request_context(db):
    user = get_user_model().objects.create_user(username="alice", password="pass")
    factory = RequestFactory()
    request = factory.post("/", HTTP_USER_AGENT="pytest-agent")
    request.META["REMOTE_ADDR"] = "127.0.0.2"

    event = log_event(
        TEST_ACTION,
        user=user,
        request=request,
        metadata={"device_id": "dev-1"},
    )

    assert event is not None
    assert event.ip == "127.0.0.2"
    assert event.user_agent == "pytest-agent"
    assert event.device_id == "dev-1"


def test_log_event_allows_explicit_overrides(db):
    user = get_user_model().objects.create_user(username="bob", password="pass")
    factory = RequestFactory()
    request = factory.post("/", HTTP_USER_AGENT="request-agent")
    request.META["REMOTE_ADDR"] = "10.0.0.9"

    event = log_event(
        TEST_ACTION,
        user=user,
        request=request,
        ip="192.168.0.10",
        user_agent="explicit-agent",
        device_id="explicit-dev",
        metadata={"k": "v"},
    )

    assert event is not None
    assert event.ip == "192.168.0.10"
    assert event.user_agent == "explicit-agent"
    assert event.device_id == "explicit-dev"
    assert event.metadata["k"] == "v"


def test_log_event_sync_returns_instance(db):
    user = get_user_model().objects.create_user(username="carol", password="pass")

    event = log_event(TEST_ACTION, user=user, metadata={"source": "test"})

    assert event is not None
    assert isinstance(event, ActLog)
    assert event.action == TEST_ACTION
    assert event.user_id == user.id
    assert event.metadata == {"source": "test"}
    assert ActLog.objects.filter(pk=event.pk).exists()


@pytest.mark.django_db(transaction=True)
def test_log_event_async_does_not_write_before_commit(settings):
    settings.ACTLOG_SYNC = False
    settings.ACTLOG_EMIT_IMMEDIATELY = False
    user = get_user_model().objects.create_user(username="dave", password="pass")

    from django.db import transaction

    with transaction.atomic():
        result = log_event(TEST_ACTION, user=user)
        assert result is None
        assert ActLog.objects.count() == 0

    assert ActLog.objects.count() == 1
    event = ActLog.objects.get()
    assert event.action == TEST_ACTION
    assert event.user_id == user.id
