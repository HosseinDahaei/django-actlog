# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Changed

- Severity constants are a first-class public API: `from actlog import Level` (prefer over `ActLog.Level`; the model alias remains for compatibility)

## [0.4.0] - 2026-07-15

### Added

- `ActLog.level` CharField with TextChoices (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`), default `INFO`, indexed
- `log_event(level=...)` parameter; omit to use `INFO`
- Colored level badges in the Django admin changelist (light and dark themes)

## [0.3.0] - 2026-07-09

### Removed

- `ActLog` model fields: `ip`, `device_id`, `user_agent`
- `log_event()` kwargs: `request`, `ip`, `device_id`, `user_agent`
- Request context auto-capture from `log_event()` — pass context via `metadata` instead

## [0.2.0] - 2026-07-09

### Changed

- `log_event()` always persists synchronously and returns the created `ActLog` instance

### Removed

- Async mode with `transaction.on_commit` signal dispatch and Celery task `actlog.write_actlog_task`
- Settings: `ACTLOG_SYNC`, `ACTLOG_EMIT_IMMEDIATELY`, `ACTLOG_CELERY_TASK`
- Optional dependency extra: `django-actlog[celery]`
- Modules: `actlog.dispatch`, `actlog.signals`, `actlog.receivers`, `actlog.tasks`

## [0.1.0] - 2026-07-09

### Added

- `ActLog` model with user FK, action string, IP, device ID, user agent, metadata JSON, and `created_at`
- `log_event()` public API with request context extraction and explicit overrides
- Sync mode (`ACTLOG_SYNC`) and async mode with `transaction.on_commit` signal dispatch
- Optional Celery task `actlog.write_actlog_task` with broker-unavailable inline fallback
- `safe_enqueue()` and `emit_on_commit()` dispatch helpers
- Read-only Django admin with optional `django-json-widget` metadata display
- Configurable settings: `ACTLOG_EMIT_IMMEDIATELY`, `ACTLOG_MODEL`, `ACTLOG_USER_RELATED_NAME`, `ACTLOG_ACTION_MAX_LENGTH`, `ACTLOG_USER_SEARCH_FIELDS`, `ACTLOG_CELERY_TASK`
- Placeholder `ActLogRequestContextMiddleware` for future request-scoped context
- Test suite with pytest-django
- GitHub Actions CI matrix (Django 4.2 / 5.0 / 6.0 × Python 3.10–3.12)

[0.4.0]: https://github.com/HosseinDahaei/django-actlog/releases/tag/v0.4.0
[0.3.0]: https://github.com/HosseinDahaei/django-actlog/releases/tag/v0.3.0
[0.2.0]: https://github.com/HosseinDahaei/django-actlog/releases/tag/v0.2.0
[0.1.0]: https://github.com/HosseinDahaei/django-actlog/releases/tag/v0.1.0
