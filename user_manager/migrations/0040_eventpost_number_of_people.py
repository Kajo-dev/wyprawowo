# Generated by Django 4.2.13 on 2024-08-23 06:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_manager", "0039_remove_eventpost_date_start"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventpost",
            name="number_of_people",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]