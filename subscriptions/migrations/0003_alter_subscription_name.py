# Generated by Django 5.1.3 on 2025-03-17 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0002_subscription_is_one_off"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="name",
            field=models.CharField(
                blank=True,
                choices=[("BASIC", "BASIC"), ("PREMIUM", "PREMIUM"), ("LATE", "LATE")],
                max_length=200,
                null=True,
            ),
        ),
    ]
