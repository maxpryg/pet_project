import logging

from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings

from pet_project.celery import app


@app.task
def send_post_creation_email(subscriber_id, subject, message):
    UserModel = get_user_model()

    try:
        subscriber = UserModel.objects.get(pk=subscriber_id)
    except UserModel.DoesNotExist:
        logging.warning(f'Tried to send verification email to '
                        f'non-existing user `{subscriber_id}`')
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [subscriber.email],
        fail_silently=False,)
