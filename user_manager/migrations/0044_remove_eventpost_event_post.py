# Generated by Django 4.2.13 on 2024-08-25 09:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user_manager", "0003_alter_profile_location"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="eventpost",
            name="event_post",
        ),
    ]
