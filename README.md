# django-actlog

Minimal, opt-in application event logging for Django MVPs.

Unlike [django-auditlog](https://github.com/jazzband/django-auditlog) (automatic model change history) or [django-easy-audit](https://github.com/soynatan/django-easy-audit) (automatic CRUD/auth hooks), **django-actlog** records events only when you explicitly call `log_event()` with a host-defined action string.

## Install

```bash
pip install django-actlog
```

Add to `INSTALLED_APPS` and migrate:

```python
INSTALLED_APPS = [
    # ...
    "actlog",
]
```

```bash
python manage.py migrate actlog
```

## Quick start

Define action constants in your project (not in the library):

```python
# myapp/audit_constants.py
LOGIN_SUCCESS = "LOGIN_SUCCESS"
OTP_SENT = "OTP_SENT"
```

Log events from your services:

```python
from actlog import log_event, Level
from myapp.audit_constants import LOGIN_SUCCESS, LOGIN_FAILED

def on_login_success(user, request, session):
    event = log_event(
        LOGIN_SUCCESS,
        user=user,
        metadata={
            "method": "otp",
            "session_id": session.id,
            "ip": request.META.get("REMOTE_ADDR"),
            "user_agent": request.META.get("HTTP_USER_AGENT", ""),
        },
    )

def on_login_failed(request, username):
    log_event(
        LOGIN_FAILED,
        level=Level.WARNING,
        metadata={"username": username, "ip": request.META.get("REMOTE_ADDR")},
    )
```

`log_event()` persists synchronously and returns the created `ActLog` instance. Pass any request or domain context via `metadata`.

Severity is set with `level` (optional; default `INFO`). Values mirror Python logging: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` (`Level`).

## Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `ACTLOG_MODEL` | `"actlog.ActLog"` | Dotted path to the log model (advanced) |
| `ACTLOG_USER_RELATED_NAME` | `"act_logs"` | `related_name` on the user FK |
| `ACTLOG_ACTION_MAX_LENGTH` | `64` | Max length for action strings |
| `ACTLOG_USER_SEARCH_FIELDS` | `("user__email",)` | Admin search lookups for the user FK |

## Django admin

Register is automatic. The admin is read-only (no add/delete). The metadata field uses a read-only JSON editor (`django-json-widget` is installed and registered automatically).

Custom user models: override `ACTLOG_USER_SEARCH_FIELDS` if `user__email` does not apply.

## Public API

```python
from actlog import log_event, ActLog, Level
from actlog.models import ActLog
from actlog.choices import Level
from actlog.services import log_event
```

## License

MIT
