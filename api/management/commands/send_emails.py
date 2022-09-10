from django.core.management.base import BaseCommand
from django.core.mail import send_mail

from blog.models import Subscriber


class Command(BaseCommand):
    help = "Commang for sending emails to blog subscribers"

    def handle(self, *args, **options):
        subject = 'Regular Saturday email'
        message = 'It is Saturday today. And we are glad to send you this mail'
        from_email = 'admin@pet_project.com'

        subscribers = Subscriber.objects.all()
        for subscriber in subscribers:
            send_mail(subject,
                        message,
                        from_email,
                        [subscriber.email],
                        fail_silently=False,
                        )
