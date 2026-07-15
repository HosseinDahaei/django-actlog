"""Admin registration for ActLog."""

from __future__ import annotations

from django.contrib import admin
from django.utils.html import format_html

from actlog.conf import get_actlog_model, get_setting
from actlog.forms import ActLogAdminForm

ActLog = get_actlog_model()


@admin.register(ActLog)
class ActLogAdmin(admin.ModelAdmin):
    """Read-only admin for application event records."""

    form = ActLogAdminForm
    list_display = ("id", "action", "colored_level", "user", "created_at")
    list_filter = ("level",)
    search_fields = tuple(get_setting("ACTLOG_USER_SEARCH_FIELDS")) + ("action",)
    ordering = ("-created_at",)
    readonly_fields = (
        "user",
        "action",
        "level",
        "created_at",
    )

    class Media:
        css = {"all": ("actlog/admin.css",)}

    @admin.display(description="Level", ordering="level")
    def colored_level(self, obj):
        level = obj.level or ActLog.Level.INFO
        return format_html(
            '<span class="actlog-level actlog-level--{}">{}</span>',
            level.lower(),
            level,
        )

    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False
