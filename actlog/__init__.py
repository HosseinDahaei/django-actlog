from __future__ import annotations

__all__ = ["log_event", "ActLog", "Level"]
__version__ = "1.0.0"


def __getattr__(name: str):
    if name == "log_event":
        from actlog.services.logging import log_event

        return log_event
    if name == "ActLog":
        from actlog.models import ActLog

        return ActLog
    if name == "Level":
        from actlog.choices import Level

        return Level
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
