import pytest
from actlog.admin import ActLogAdmin
from actlog.models import ActLog
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import Client


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="password",
    )


@pytest.fixture
def actlog_entry(db):
    user = get_user_model().objects.create_user(username="viewer", password="pass")
    return ActLog.objects.create(
        user=user,
        action="LOGIN_SUCCESS",
        metadata={"method": "otp"},
    )


def test_actlog_registered_in_admin():
    assert ActLog in admin.site._registry
    assert isinstance(admin.site._registry[ActLog], ActLogAdmin)


def test_admin_has_no_add_or_delete_permission(admin_user):
    model_admin = admin.site._registry[ActLog]
    request = type("Request", (), {"user": admin_user})()

    assert model_admin.has_add_permission(request) is False
    assert model_admin.has_delete_permission(request) is False


def test_admin_fields_are_readonly(admin_user, actlog_entry):
    model_admin = admin.site._registry[ActLog]
    readonly = model_admin.get_readonly_fields(request=None, obj=actlog_entry)

    assert "action" in readonly
    assert "user" in readonly
    assert "created_at" in readonly


def test_admin_metadata_field_is_disabled(admin_user, actlog_entry):
    model_admin = admin.site._registry[ActLog]
    form = model_admin.get_form(request=None)(instance=actlog_entry)

    assert form.fields["metadata"].disabled is True


def test_admin_change_view_renders(admin_user, actlog_entry):
    client = Client()
    client.force_login(admin_user)
    url = f"/admin/actlog/actlog/{actlog_entry.pk}/change/"
    response = client.get(url)
    assert response.status_code == 200
    assert "LOGIN_SUCCESS" in response.content.decode()


def test_admin_changelist_renders(admin_user, actlog_entry):
    client = Client()
    client.force_login(admin_user)
    response = client.get("/admin/actlog/actlog/")
    assert response.status_code == 200
    assert "LOGIN_SUCCESS" in response.content.decode()
