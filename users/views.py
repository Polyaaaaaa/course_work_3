# users\views.py
import secrets

from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages

from config.settings import EMAIL_HOST_USER
from .forms import CustomUserCreationForm
from .models import CustomUser


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
        scheme = self.request.scheme  # http или https
        url = f"{scheme}://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Для подтверждения вашей почты перейдите по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        messages.success(self.request, "На вашу почту отправлено письмо с подтверждением.")
        return super().form_valid(form)


def email_confirm_view(request, token):
    try:
        user = CustomUser.objects.get(token=token)
        user.is_active = True
        user.token = ""  # Очистить токен после подтверждения
        user.save()
        messages.success(request, "Email успешно подтвержден. Теперь вы можете войти.")
    except CustomUser.DoesNotExist:
        messages.error(request, "Неверный токен.")

    return redirect("users:login")


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    success_url = reverse_lazy("mailing_management:home")

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            messages.error(self.request, "Ваш email не подтвержден. Пожалуйста, проверьте почту.")
            return HttpResponseRedirect(reverse_lazy("users:login"))  # Перенаправляем обратно на вход
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    template_name = "users/logout.html"
    next_page = reverse_lazy(
        "users:register"
    )  # Перенаправление на страницу регистрации после выхода


class PasswordResetView_(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'  # Шаблон для письма
    subject_template_name = 'users/password_reset_subject.txt'  # Тема письма
    success_url = reverse_lazy('users:password_reset_done')


class PasswordResetDoneView_(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class PasswordResetConfirmView_(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

class PasswordResetCompleteView_(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
