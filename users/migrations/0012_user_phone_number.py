# Generated by Django 5.1.3 on 2025-03-14 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0011_user_document_verified_verificationsession"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="phone_number",
            field=models.TextField(blank=True, default="", null=True),
        ),
    ]
