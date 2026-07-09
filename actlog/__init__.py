from __future__ import annotations

__all__ = ["log_event", "ActLog"]
__version__ = "0.3.0"


def __getattr__(name: str):
    if name == "log_event":
        from actlog.services.logging import log_event

        return log_event
    if name == "ActLog":
        from actlog.models import ActLog

        return ActLog
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
