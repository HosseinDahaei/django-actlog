import pytest


@pytest.fixture(autouse=True)
def _sync_actlog(settings):
    settings.ACTLOG_SYNC = True
    settings.ACTLOG_EMIT_IMMEDIATELY = True
