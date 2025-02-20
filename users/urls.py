# users/urls.py
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from mailing_management.views import HomeView
from users.views import RegisterView, CustomLoginView, CustomLogoutView

app_name = "users"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),  # URL для главной страницы
    path(
        "register/",
        RegisterView.as_view(template_name="users/register.html"),
        name="register",
    ),
    path("login/", CustomLoginView.as_view(), name="login"),
    path(
        "logout/",
        CustomLogoutView.as_view(next_page="mailing_management:home"),
        name="logout",
    ),
]
