# Generated by Django 5.1.6 on 2025-02-20 09:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "mailing_management",
            "0003_alter_mailingclient_options_mailingclient_user_and_more",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="newsletter",
            options={
                "ordering": ["message"],
                "permissions": [
                    ("can_unpublish_newsletter", "Can unpublish newsletter"),
                    ("can_delete_newsletter", "Can delete newsletter"),
                    ("view_all_newsletters", "View all newsletters"),
                ],
                "verbose_name": "рассылка",
                "verbose_name_plural": "рассылки",
            },
        ),
        migrations.AddField(
            model_name="mailingclient",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="clients",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="newsletter",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="newsletters",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
