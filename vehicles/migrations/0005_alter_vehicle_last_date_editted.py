# Generated by Django 5.1.3 on 2024-11-16 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vehicles", "0004_vehicle_last_date_editted"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicle",
            name="last_date_editted",
            field=models.DateTimeField(auto_now=True),
        ),
    ]