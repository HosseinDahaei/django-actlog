from actlog.choices import Level
from actlog.models import ActLog
from actlog.services.logging import log_event
from django.contrib.auth import get_user_model

TEST_ACTION = "TEST_ACTION"


def test_log_event_returns_instance(db):
    user = get_user_model().objects.create_user(username="carol", password="pass")

    event = log_event(TEST_ACTION, user=user, metadata={"source": "test"})

    assert event is not None
    assert isinstance(event, ActLog)
    assert event.action == TEST_ACTION
    assert event.level == Level.INFO
    assert event.user_id == user.id
    assert event.metadata == {"source": "test"}
    assert ActLog.objects.filter(pk=event.pk).exists()


def test_log_event_stores_metadata_as_is(db):
    user = get_user_model().objects.create_user(username="dana", password="pass")
    metadata = {
        "ip": "127.0.0.1",
        "user_agent": "pytest-agent",
        "device_id": "dev-1",
        "method": "otp",
    }

    event = log_event(TEST_ACTION, user=user, metadata=metadata)

    assert event.metadata == metadata


def test_log_event_defaults_level_to_info(db):
    event = log_event(TEST_ACTION)

    assert event.level == Level.INFO


def test_log_event_persists_explicit_level(db):
    user = get_user_model().objects.create_user(username="erin", password="pass")

    warning = log_event(TEST_ACTION, user=user, level=Level.WARNING)
    error = log_event(TEST_ACTION, user=user, level=Level.ERROR)

    assert warning.level == Level.WARNING
    assert error.level == Level.ERROR


def test_actlog_level_alias_matches_shared_level():
    assert ActLog.Level is Level
    assert ActLog.Level.INFO == Level.INFO
