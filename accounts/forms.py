from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name',
                  'birth_date', 'city')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class LoginForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        verification_error_msg = """We cannot log you in, until you don't
        verify your email. Please, check your email box and follow the
        confimation link."""

        blocked_user_error_msg = """You account is blocked. Please contact
        system administrator."""

        if not user.email_verified:
            raise ValidationError(verification_error_msg,
                                  code='email_not_verified')

        if user.blocked:
            raise ValidationError(blocked_user_error_msg, code='user_blocked')
