# Generated by Django 4.2.13 on 2024-09-05 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0044_remove_eventpost_event_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='requires_text_input',
            field=models.BooleanField(default=False),
        ),
    ]
