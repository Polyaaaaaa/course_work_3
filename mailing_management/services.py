# services.py
from .models import MailingClient, MessageManagement, Newsletter, NewsletterAttempt
from django.core.mail import send_mail
from django.conf import settings


class ClientService:

    @staticmethod
    def get_client_list(client_id):
        # Получаем всех клиентов с указанным идентификатором
        clients = MailingClient.objects.filter(id=client_id)
        return clients


class MessageService:

    @staticmethod
    def get_message_list(message_id):
        # Получаем все продукты в указанной категории
        messages = MessageManagement.objects.filter(id=message_id)
        return messages


class NewsletterService:

    @staticmethod
    def get_newsletter_list(newsletter_id):
        # Получаем все продукты в указанной категории
        newsletters = Newsletter.objects.filter(id=newsletter_id)
        return newsletters


def send_newsletter(newsletter):
    subject = newsletter.message.subject
    body = newsletter.message.body
    clients = [client.email for client in newsletter.clients.all()]
    for client in clients:
        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [client],
            )
            # Создаем запись об успешной попытке
            NewsletterAttempt.objects.create(status="successful", newsletter=newsletter)
        except Exception as e:
            # Создаем запись о неуспешной попытке
            NewsletterAttempt.objects.create(
                status="failed", server_response=str(e), newsletter=newsletter
            )
