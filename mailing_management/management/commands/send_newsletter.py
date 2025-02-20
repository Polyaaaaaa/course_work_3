from django.core.management.base import BaseCommand
from mailing_management.models import Newsletter
from mailing_management.services import send_newsletter


class Command(BaseCommand):
    help = "Send a newsletter by its ID"

    def add_arguments(self, parser):
        parser.add_argument("newsletter_id", type=int, help="ID of the newsletter to send")

    def handle(self, *args, **options):
        newsletter_id = options["newsletter_id"]
        newsletter = Newsletter.objects.get(id=newsletter_id)

        # Отправляем рассылку
        send_newsletter(newsletter)

        self.stdout.write(self.style.SUCCESS(f"Newsletter {newsletter_id} sent successfully!"))
