# admin.py
from django.contrib import admin
from .models import MailingClient, MessageManagement, Newsletter


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


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = (
        "beginning_date",
        "end_date",
        "status",
        "message",
        "get_clients",
    )
    list_filter = (
        "status",
        "beginning_date",
        "end_date",
    )
    search_fields = (
        "message__subject",
        "clients__email",
    )

    def get_clients(self, obj):
        # Метод для отображения списка клиентов в админке
        return ", ".join([client.email for client in obj.clients.all()])
    get_clients.short_description = "Получатели"

# Не забудьте зарегистрировать связанные модели, если они еще не зарегистрированы
