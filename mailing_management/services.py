# services.py
from .models import MailingClient, MessageManagement, Newsletter


class ClientService:

    @staticmethod
    def get_client_list(client_id):
        # Получаем все продукты в указанной категории
        clients = MailingClient.objects.filter(category_id=client_id)
        return clients