# Generated by Django 5.0.7 on 2024-11-13 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("PCNs", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="pcn",
            name="is_paid",
            field=models.BooleanField(default=False),
        ),
    ]
