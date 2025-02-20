from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        help_text="Необязательное поле. Введите ваш номер телефона.",
    )
    username = forms.CharField(max_length=50, required=True)

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "password1",
            "password2",
        )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен состоять только из цифр")
        return phone_number


class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        subject = "Восстановление пароля"
        message = "Пройдите по ссылке, чтобы восстановить пароль: {}".format(
            context["protocol"]
            + "://"
            + context["domain"]
            + reverse(
                "users:password_reset_confirm",
                kwargs={
                    "uidb64": urlsafe_base64_encode(force_bytes(context["user"].pk)),
                    "token": default_token_generator.make_token(context["user"]),
                },
            )
        )
        send_mail(subject, message, from_email, [to_email])


class CustomSetPasswordForm(SetPasswordForm):
    pass
