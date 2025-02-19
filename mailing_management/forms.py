from django.core.exceptions import ValidationError
from django.forms import BooleanField, ModelForm
from mailing_management.models import MailingClient, MessageManagement, Newsletter


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class MailingClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = MailingClient
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Получаем текущего получателя
        super().__init__(*args, **kwargs)

    def clean_comment(self):
        comment = self.cleaned_data["comment"]
        forbidden_words = [
            "казино",
            "криптовалюта",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]
        for word in forbidden_words:
            if word in comment:
                raise ValidationError(
                    "Ваше описание содержит слова, которые включены в список запрещенных слов."
                )
        return comment


class MailingClientModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = MailingClient
        fields = ('full_name',)


class MessageManagementForm(StyleFormMixin, ModelForm):
    class Meta:
        model = MessageManagement
        fields = "__all__"

    def clean_subject(self):
        subject = self.cleaned_data['subject']
        forbidden_words = [
            "казино",
            "криптовалюта",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]
        for word in forbidden_words:
            if word in subject:
                raise ValidationError(
                    "Ваша тема письма содержит слова, которые включены в список запрещенных."
                )
        return subject

    def clean_body(self):
        body = self.cleaned_data['body']
        forbidden_words = [
            "казино",
            "криптовалюта",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]
        for word in forbidden_words:
            if word in body:
                raise ValidationError(
                    "Тело письма содержит слова, которые включены в список запрещенных."
                )
        return body


class MessageManagementModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = MessageManagement
        fields = ('subject',)


class NewsletterForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Newsletter
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Получаем текущего пользователя
        super().__init__(*args, **kwargs)

    def clean_message(self):
        message = self.cleaned_data["message"]
        if not message:
            raise ValidationError("Сообщение не может быть пустым.")
        return message

    def clean_clients(self):
        clients = self.cleaned_data["clients"]
        if not clients:
            raise ValidationError("Вы должны выбрать хотя бы одного клиента для рассылки.")
        return clients


class NewsletterModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Newsletter
        fields = ('status',)
