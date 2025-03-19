# Generated by Django 5.1.6 on 2025-02-24 12:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "mailing_management",
            "0006_alter_mailingclient_owner_alter_mailingclient_user",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="newsletterstatistics",
            name="user",
        ),
        migrations.AddField(
            model_name="newsletterstatistics",
            name="newsletter",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="statistics",
                to="mailing_management.newsletter",
            ),
        ),
    ]
