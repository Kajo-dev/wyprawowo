# Generated by Django 4.2.13 on 2024-08-23 05:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("user_manager", "0037_postattachment"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventpost",
            name="date_end",
            field=models.DateTimeField(
                blank=True, default=django.utils.timezone.now, null=True
            ),
        ),
        migrations.AddField(
            model_name="eventpost",
            name="date_start",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]