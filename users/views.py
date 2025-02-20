# users\views.py
import secrets

from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from config.settings import EMAIL_HOST_USER
from .forms import CustomUserCreationForm


# Create your views here.
class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("mailing_management:home")

    def form_valid(self, form):
        user = form.save()
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Для подтверждения вашей почты перейдите по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    success_url = reverse_lazy(
        "mailing_management:home"
    )  # Перенаправление после успешного входа


class CustomLogoutView(LogoutView):
    template_name = "users/logout.html"
    next_page = reverse_lazy(
        "users:register"
    )  # Перенаправление на страницу регистрации после выхода


class PasswordResetView_(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')


class PasswordResetDoneView_(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class PasswordResetConfirmView_(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class PasswordResetCompleteView_(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
