# Generated by Django 4.2.13 on 2024-07-09 10:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_manager", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="last_name",
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]