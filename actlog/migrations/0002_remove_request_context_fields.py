from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("actlog", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="actlog",
            name="ip",
        ),
        migrations.RemoveField(
            model_name="actlog",
            name="device_id",
        ),
        migrations.RemoveField(
            model_name="actlog",
            name="user_agent",
        ),
    ]
