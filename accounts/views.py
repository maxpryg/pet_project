from django.shortcuts import render
from django.views.generic import (CreateView,
                                  UpdateView,
                                  TemplateView,
                                  RedirectView,)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model

from django.urls import reverse_lazy

from accounts.forms import CustomUserCreationForm, LoginForm
from accounts.tokens import token_generator
from accounts.tasks import send_user_activation_email


user_model = get_user_model()


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:check_email")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        user = form.save()
        user.save()
        send_user_activation_email.delay(user.id)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginForm


class ProfileView(SuccessMessageMixin, UpdateView):
    model = user_model
    fields = ['first_name', 'last_name', 'birth_date', 'city']
    template_name = 'accounts/profile.html'
    success_message = 'Profile has been successfully updated!!!!'

    def get_queryset(self):
        return user_model.objects.filter(id=self.request.user.id)


class ActivateView(RedirectView):
    url = reverse_lazy('accounts:success')

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = user_model.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            login(request, user)
            return super().get(request, uidb64, token)
        else:
            return render(request,
                          'registration/activate_account_invalid.html')


class CheckEmailView(TemplateView):
    template_name = 'registration/check_email.html'


class SuccessView(TemplateView):
    template_name = 'registration/success.html'
