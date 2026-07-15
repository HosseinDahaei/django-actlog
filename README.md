# django-actlog

Minimal, opt-in application event logging for Django MVPs.

Unlike [django-auditlog](https://github.com/jazzband/django-auditlog) (automatic model change history) or [django-easy-audit](https://github.com/soynatan/django-easy-audit) (automatic CRUD/auth hooks), **django-actlog** records events only when you explicitly call `log_event()` with a host-defined action string.

## Install

```bash
pip install django-actlog
```

Optional extras:

```bash
pip install "django-actlog[admin]"    # pretty JSON metadata in Django admin
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
from actlog import log_event
from actlog.models import ActLog
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
        level=ActLog.Level.WARNING,
        metadata={"username": username, "ip": request.META.get("REMOTE_ADDR")},
    )
```

`log_event()` persists synchronously and returns the created `ActLog` instance. Pass any request or domain context via `metadata`.

Severity is set with `level` (optional; default `INFO`). Values mirror Python logging: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` (`ActLog.Level`).

## Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `ACTLOG_MODEL` | `"actlog.ActLog"` | Dotted path to the log model (advanced) |
| `ACTLOG_USER_RELATED_NAME` | `"act_logs"` | `related_name` on the user FK |
| `ACTLOG_ACTION_MAX_LENGTH` | `64` | Max length for action strings |
| `ACTLOG_USER_SEARCH_FIELDS` | `("user__email",)` | Admin search lookups for the user FK |

## Django admin

Register is automatic. The admin is read-only (no add/delete).

For a JSON editor on the metadata field:

```bash
pip install "django-actlog[admin]"
```

Custom user models: override `ACTLOG_USER_SEARCH_FIELDS` if `user__email` does not apply.

## Public API

```python
from actlog import log_event, ActLog
from actlog.models import ActLog
from actlog.services import log_event
```

## Migrating from an internal `apps.audit` app

1. `pip install django-actlog`
2. Replace `"apps.audit"` with `"actlog"` in `INSTALLED_APPS`
3. Keep domain action constants in your project (e.g. `apps/core/audit_constants.py`)
4. Update imports:
   - `from apps.audit.services import log_event` → `from actlog import log_event`
   - `from apps.audit.models import AuditLog` → `from actlog.models import ActLog`
5. Remove any `ACTLOG_SYNC`, `ACTLOG_EMIT_IMMEDIATELY`, or Celery task configuration — logging is always synchronous.

**v0.1.0** targets new installs. Existing `audit_auditlog` tables require a custom data migration if you need to preserve history under a new table name (`actlog_actlog`).

## License

MIT
