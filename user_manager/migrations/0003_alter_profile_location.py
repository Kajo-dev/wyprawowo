# Generated by Django 4.2.13 on 2024-09-09 17:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_manager", "0002_profile_location"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="location",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]