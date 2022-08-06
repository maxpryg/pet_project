import logging

from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from celery import shared_task

# from pet_project.celery import app


# @app.task
@shared_task()
def send_post_creation_email(subscriber_id, subject, message):
    UserModel = get_user_model()

    try:
        subscriber = UserModel.objects.get(pk=subscriber_id)
    except UserModel.DoesNotExist:
        logging.warning(f'Tried to send verification email to '
                        f'non-existing user `{subscriber}`')
    send_mail(
        subject,
        message,
        'maxpryg@gmail.com',
        [subscriber.email],
        fail_silently=False,)

def send_activation_email(self, request, user):
    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    message = render_to_string(
        'registration/activate_account.html',
        {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user),
        }
    )
