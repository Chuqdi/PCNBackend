# Generated by Django 5.1.3 on 2025-03-18 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0013_user_document_verification_with_sucess"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="document_verification_with_sucess",
            new_name="document_verification_with_success",
        ),
    ]
