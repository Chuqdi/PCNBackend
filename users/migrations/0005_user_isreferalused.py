# Generated by Django 5.1.3 on 2024-11-22 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_devicetoken"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="isReferalUsed",
            field=models.BooleanField(default=False),
        ),
    ]
