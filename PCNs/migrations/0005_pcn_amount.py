# Generated by Django 5.1.3 on 2024-11-20 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("PCNs", "0004_alter_pcn_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="pcn",
            name="amount",
            field=models.IntegerField(default=0),
        ),
    ]
