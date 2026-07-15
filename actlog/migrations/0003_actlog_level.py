from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("actlog", "0002_remove_request_context_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="actlog",
            name="level",
            field=models.CharField(
                choices=[
                    ("DEBUG", "Debug"),
                    ("INFO", "Info"),
                    ("WARNING", "Warning"),
                    ("ERROR", "Error"),
                    ("CRITICAL", "Critical"),
                ],
                db_index=True,
                default="INFO",
                max_length=16,
            ),
        ),
    ]
