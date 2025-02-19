# services.py
from .models import MailingClient, MessageManagement, Newsletter


class ClientService:

    @staticmethod
    def get_client_list(client_id):
        # Получаем все продукты в указанной категории
        clients = MailingClient.objects.filter(client_id=client_id)
        return clients


class MessageService:

    @staticmethod
    def get_client_list(message_id):
        # Получаем все продукты в указанной категории
        messages = MessageManagement.objects.filter(message_id=message_id)
        return messages
