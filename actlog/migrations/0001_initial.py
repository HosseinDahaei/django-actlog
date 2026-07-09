# Generated manually for django-actlog 0.1.0

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ActLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("action", models.CharField(db_index=True, max_length=64)),
                ("ip", models.GenericIPAddressField(blank=True, null=True)),
                ("device_id", models.CharField(blank=True, default="", max_length=255)),
                ("user_agent", models.TextField(blank=True, default="")),
                ("metadata", models.JSONField(blank=True, default=dict)),
                (
                    "created_at",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        editable=False,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="act_logs",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "indexes": [
                    models.Index(
                        fields=["action", "-created_at"],
                        name="actlog_action_created_idx",
                    ),
                    models.Index(
                        fields=["user", "-created_at"],
                        name="actlog_user_created_idx",
                    ),
                ],
            },
        ),
    ]
