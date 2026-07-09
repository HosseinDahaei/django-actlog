# django-actlog

Minimal, opt-in application event logging for Django MVPs.

Unlike [django-auditlog](https://github.com/jazzband/django-auditlog) (automatic model change history) or [django-easy-audit](https://github.com/soynatan/django-easy-audit) (automatic CRUD/auth hooks), **django-actlog** records events only when you explicitly call `log_event()` with a host-defined action string.

## Install

```bash
pip install django-actlog
```

Optional extras:

```bash
pip install "django-actlog[celery]"   # async Celery persistence
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
from myapp.audit_constants import LOGIN_SUCCESS

def on_login_success(user, request, session):
    log_event(
        LOGIN_SUCCESS,
        user=user,
        request=request,
        metadata={"method": "otp", "session_id": session.id},
    )
```

`log_event()` captures request context when `request` is provided:

- `ip` from `request.META["REMOTE_ADDR"]`
- `user_agent` from `request.META.get("HTTP_USER_AGENT", "")`
- `device_id` from the explicit argument or `metadata["device_id"]`

Explicit arguments always override request-derived values.

## Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `ACTLOG_SYNC` | `False` | Persist synchronously and return the `ActLog` instance |
| `ACTLOG_EMIT_IMMEDIATELY` | `False` | Skip `transaction.on_commit` for signal dispatch (useful in tests) |
| `ACTLOG_MODEL` | `"actlog.ActLog"` | Dotted path to the log model (advanced) |
| `ACTLOG_USER_RELATED_NAME` | `"act_logs"` | `related_name` on the user FK |
| `ACTLOG_ACTION_MAX_LENGTH` | `64` | Max length for action strings |
| `ACTLOG_USER_SEARCH_FIELDS` | `("user__email",)` | Admin search lookups for the user FK |
| `ACTLOG_CELERY_TASK` | auto | Dotted path to a custom Celery task |

**Migrating from an internal audit app:** rename `AUDIT_SYNC` → `ACTLOG_SYNC` and `EMIT_SIGNALS_IMMEDIATELY` → `ACTLOG_EMIT_IMMEDIATELY` in your host settings. The library reads only `ACTLOG_*` names.

## Async mode (default)

By default, `log_event()` emits an internal signal after the current database transaction commits. A receiver enqueues `actlog.write_actlog_task` via Celery when available.

If the broker is unavailable, the library falls back to inline execution and logs a warning — audit logging never breaks your request.

```python
# settings.py (production)
ACTLOG_SYNC = False
```

### Celery setup

```bash
pip install "django-actlog[celery]"
```

Ensure `actlog` is in `INSTALLED_APPS` and run a Celery worker that autodiscovers tasks:

```python
# celery.py
app.autodiscover_tasks()
```

The stable task name is `actlog.write_actlog_task`.

### Without Celery

When Celery is not installed, the receiver persists logs inline after commit. For tests or simple deployments, use sync mode:

```python
ACTLOG_SYNC = True
```

## Django admin

Register is automatic. The admin is read-only (no add/delete).

For a JSON editor on the metadata field:

```bash
pip install "django-actlog[admin]"
```

Custom user models: override `ACTLOG_USER_SEARCH_FIELDS` if `user__email` does not apply.

## Testing

In test settings, enable synchronous persistence:

```python
# conftest.py or settings/test.py
ACTLOG_SYNC = True
ACTLOG_EMIT_IMMEDIATELY = True
```

Or with pytest:

```python
@pytest.fixture(autouse=True)
def _sync_actlog(settings):
    settings.ACTLOG_SYNC = True
    settings.ACTLOG_EMIT_IMMEDIATELY = True
```

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
5. Rename settings: `AUDIT_SYNC` → `ACTLOG_SYNC`, `EMIT_SIGNALS_IMMEDIATELY` → `ACTLOG_EMIT_IMMEDIATELY`

**v0.1.0** targets new installs. Existing `audit_auditlog` tables require a custom data migration if you need to preserve history under a new table name (`actlog_actlog`).

## License

MIT
