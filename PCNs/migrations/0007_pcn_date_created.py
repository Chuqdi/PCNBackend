# Generated by Django 5.1.3 on 2025-03-18 09:25

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("PCNs", "0006_pcn_is_denied"),
    ]

    operations = [
        migrations.AddField(
            model_name="pcn",
            name="date_created",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
