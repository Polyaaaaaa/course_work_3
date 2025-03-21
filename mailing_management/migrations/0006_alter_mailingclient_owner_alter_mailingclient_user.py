# Generated by Django 5.1.6 on 2025-02-24 12:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "mailing_management",
            "0005_alter_mailingclient_options_newsletterattempt_and_more",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailingclient",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="added_clients",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец (кто добавил)",
            ),
        ),
        migrations.AlterField(
            model_name="mailingclient",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="mailing_clients",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь (если зарегистрирован)",
            ),
        ),
    ]
