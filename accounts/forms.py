from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError

from .models import CustomUser
from .tokens import token_generator


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'birth_date', 'city')

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

        user.email_user(subject, message, html_message=message)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class LoginForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        error_msg = """We cannot log you in, until you don't verify your email.
                Please, check your email box and follow the confimation link."""

        if not user.email_verified:
            raise ValidationError(error_msg, code='email_not_verified')
