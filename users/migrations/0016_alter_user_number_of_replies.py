# Generated by Django 3.2.5 on 2024-06-16 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_user_number_of_replies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='number_of_replies',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
