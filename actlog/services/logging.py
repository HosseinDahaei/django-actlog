"""Audit logging service entrypoint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from actlog.conf import get_actlog_model

if TYPE_CHECKING:
    from actlog.models import ActLog


def _resolve_request_context(
    *,
    request=None,
    metadata: dict | None = None,
    ip: str | None = None,
    device_id: str | None = None,
    user_agent: str | None = None,
) -> tuple[dict, str | None, str, str]:
    request_ip = None
    request_ua = ""
    if request is not None:
        request_ip = request.META.get("REMOTE_ADDR")
        request_ua = request.META.get("HTTP_USER_AGENT", "")

    resolved_metadata = dict(metadata or {})
    resolved_device_id = device_id or resolved_metadata.get("device_id", "")
    resolved_ip = ip if ip is not None else request_ip
    resolved_user_agent = user_agent if user_agent is not None else request_ua
    return resolved_metadata, resolved_ip, resolved_device_id, resolved_user_agent


def _persist_actlog(
    action: str,
    *,
    user_id: int | None = None,
    metadata: dict | None = None,
    ip: str | None = None,
    device_id: str | None = None,
    user_agent: str | None = None,
) -> ActLog:
    model = get_actlog_model()
    return model.objects.create(
        user_id=user_id,
        action=action,
        ip=ip,
        device_id=device_id or "",
        user_agent=user_agent or "",
        metadata=dict(metadata or {}),
    )


def log_event(
    action: str,
    *,
    user=None,
    request=None,
    metadata: dict | None = None,
    ip: str | None = None,
    device_id: str | None = None,
    user_agent: str | None = None,
) -> ActLog:
    """Persist an application event synchronously and return the created ActLog."""
    resolved_metadata, resolved_ip, resolved_device_id, resolved_user_agent = (
        _resolve_request_context(
            request=request,
            metadata=metadata,
            ip=ip,
            device_id=device_id,
            user_agent=user_agent,
        )
    )
    user_id = user.id if user is not None else None
    payload = {
        "action": action,
        "user_id": user_id,
        "metadata": resolved_metadata,
        "ip": resolved_ip,
        "device_id": resolved_device_id,
        "user_agent": resolved_user_agent,
    }
    return _persist_actlog(**payload)
