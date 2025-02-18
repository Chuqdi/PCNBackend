# Generated by Django 5.1.3 on 2024-12-07 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, unique=True)),
                ('percentage_off', models.IntegerField()),
                ('duration', models.CharField(choices=[('ONCE', 'once'), ('FOREVER', 'forever'), ('REPEATING', 'repeating')], default='forever', max_length=400)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
