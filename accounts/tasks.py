from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.conf import settings

from pet_project.celery import app
from accounts.tokens import token_generator


user_model = get_user_model()


@app.task
def send_user_activation_email(user_id):
    user = user_model.objects.get(id=user_id)
    current_site = Site.objects.get_current()
    subject = 'Activate Your Account'
    message = render_to_string(
        'registration/activate_account.html',
        {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user),
        })

    send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
            )
