# Generated by Django 5.1.3 on 2024-12-23 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_notifications", "0003_notification_screen"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="screen",
            field=models.TextField(
                blank=True,
                choices=[("Home", "Home"), ("Ticket", "Ticket"), ("Plans", "Plans")],
                null=True,
            ),
        ),
    ]
