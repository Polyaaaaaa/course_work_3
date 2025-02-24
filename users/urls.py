from django.urls import path
from mailing_management.views import HomeView
from users import views
from users.views import (
    RegisterView, CustomLoginView, CustomLogoutView,
    PasswordResetView_, PasswordResetDoneView_, PasswordResetConfirmView_, PasswordResetCompleteView_
)

app_name = "users"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(next_page="mailing_management:home"), name="logout"),

    # Подтверждение email
    path("email-confirm/<str:token>/", views.email_confirm_view, name="email_confirm"),

    # Восстановление пароля
    path('password-reset/', PasswordResetView_.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView_.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView_.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView_.as_view(), name='password_reset_complete'),
]
