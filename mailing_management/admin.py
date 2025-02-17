# admin.py
from django.contrib import admin
from .models import MailingClient, MessageManagement


# Register your models here.
@admin.register(MailingClient)
class MailingClientAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "full_name",
        "comment",
    )
    list_filter = ("email", "full_name")


@admin.register(MessageManagement)
class MessageManagementAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "body",
    )
    list_filter = (
        "subject",
    )