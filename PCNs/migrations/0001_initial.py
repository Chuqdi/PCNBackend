# Generated by Django 5.0.7 on 2024-11-13 13:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("vehicles", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PCN",
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
                ("ticket_type", models.CharField(max_length=300)),
                ("pcn", models.TextField()),
                ("date_of_notice", models.DateField()),
                (
                    "front_ticket_image",
                    models.ImageField(upload_to="front_ticket_image/"),
                ),
                (
                    "second_ticket_image",
                    models.ImageField(upload_to="second_ticket_image/"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "vehicle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vehicles.vehicle",
                    ),
                ),
            ],
        ),
    ]
