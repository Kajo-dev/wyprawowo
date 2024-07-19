# Generated by Django 4.2.13 on 2024-07-16 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("user_manager", "0004_delete_usercharacteristics"),
    ]

    operations = [
        migrations.CreateModel(
            name="Answers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("answer1", models.TextField(blank=True, null=True)),
                ("answer2", models.TextField(blank=True, null=True)),
                ("answer3", models.TextField(blank=True, null=True)),
                (
                    "profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answers",
                        to="user_manager.profile",
                    ),
                ),
            ],
        ),
    ]