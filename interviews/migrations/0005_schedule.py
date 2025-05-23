# Generated by Django 5.1.4 on 2025-04-12 05:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("interviews", "0004_counselor_remove_telecaller_role"),
    ]

    operations = [
        migrations.CreateModel(
            name="Schedule",
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
                ("scheduled_on", models.DateTimeField()),
                ("remark", models.TextField()),
                (
                    "candidate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="interviews.telecaller",
                    ),
                ),
            ],
        ),
    ]
