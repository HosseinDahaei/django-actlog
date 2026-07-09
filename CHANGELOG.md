# Changelog

All notable changes to this project will be documented in this file.

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

[0.1.0]: https://github.com/HosseinDahaei/django-actlog/releases/tag/v0.1.0
