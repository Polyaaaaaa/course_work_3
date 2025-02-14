from django.core.management.base import BaseCommand

from mailing_management.models import MailingClient


class Command(BaseCommand):
    help = "Add test clients to the database"

    def handle(self, *args, **kwargs):
        client, created = MailingClient.objects.get_or_create(
            email="test_email@example.com",
            defaults={
                "full_name": "Test Name",
                "comment": "This is a test client"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created client: {client.full_name}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Client with email {client.email} already exists'))





