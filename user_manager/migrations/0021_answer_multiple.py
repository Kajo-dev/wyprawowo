# Generated by Django 4.2.13 on 2024-07-18 09:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_manager", "0020_alter_answer_question"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="multiple",
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]