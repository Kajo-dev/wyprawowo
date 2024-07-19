# Generated by Django 4.2.13 on 2024-07-18 09:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_manager", "0021_answer_multiple"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="answer",
            name="multiple",
        ),
        migrations.AddField(
            model_name="question",
            name="multiple_answer",
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
