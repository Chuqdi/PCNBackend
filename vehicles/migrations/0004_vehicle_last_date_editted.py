# Generated by Django 5.1.3 on 2024-11-15 09:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vehicles", "0003_alter_vehicle_color_alter_vehicle_vehicle_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="vehicle",
            name="last_date_editted",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
