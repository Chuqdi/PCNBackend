# Generated by Django 5.1.3 on 2024-11-29 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_isreferalused'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='home_address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone_number',
        ),
    ]
