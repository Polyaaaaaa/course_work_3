# users\views.py
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm


# Create your views here.
class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("mailing_management:home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = "Добро пожаловать в наш сервис!"
        message = "Спасибо, что зарегистрировались в нашем сервере!"
        from_email = "polina.syatraikina@yandex.ru"
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


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
