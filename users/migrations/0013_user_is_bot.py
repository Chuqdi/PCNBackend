# Generated by Django 3.2.5 on 2024-06-11 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_bot',
            field=models.BooleanField(default=False),
        ),
    ]
