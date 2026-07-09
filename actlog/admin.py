"""Admin registration for ActLog."""

from __future__ import annotations

from django.contrib import admin

from actlog.conf import get_actlog_model, get_setting
from actlog.forms import ActLogAdminForm

ActLog = get_actlog_model()


@admin.register(ActLog)
class ActLogAdmin(admin.ModelAdmin):
    """Read-only admin for application event records."""

    form = ActLogAdminForm
    list_display = ("id", "action", "user", "created_at")
    search_fields = tuple(get_setting("ACTLOG_USER_SEARCH_FIELDS")) + ("action",)
    ordering = ("-created_at",)
    readonly_fields = (
        "user",
        "action",
        "created_at",
    )

    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False
