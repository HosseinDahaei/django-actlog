"""Forms for actlog admin."""

from __future__ import annotations

from django import forms
from django_json_widget.widgets import JSONEditorWidget

from actlog.conf import get_actlog_model

_METADATA_VIEW_OPTIONS = {
    "mode": "view",
    "modes": ["view"],
    "mainMenuBar": False,
    "navigationBar": True,
    "search": True,
}


class ActLogAdminForm(forms.ModelForm):
    """Read-only actlog detail form; metadata uses JSONEditor."""

    class Meta:
        model = get_actlog_model()
        fields = "__all__"
        widgets = {
            "metadata": JSONEditorWidget(
                options=_METADATA_VIEW_OPTIONS,
                height="480px",
                width="100%",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        metadata_field = self.fields.get("metadata")
        if metadata_field is not None:
            metadata_field.disabled = True
