# Generated by Django 3.0.4 on 2020-03-24 15:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("social_network", "0002_auto_20200323_1930"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bot",
            name="user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bot",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
