# services.py
from .models import MailingClient, MessageManagement, Newsletter


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
