# Generated by Django 4.2.13 on 2024-07-19 10:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_manager", "0023_profile_avatar_profile_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="multiple_answer",
            field=models.BooleanField(default=False),
        ),
    ]
