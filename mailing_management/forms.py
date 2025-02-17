from django.core.exceptions import ValidationError
from django.forms import BooleanField, ModelForm
from mailing_management.models import MailingClient, MessageManagement


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

    # def clean_price(self):
    #     price = self.cleaned_data["price"]
    #     if price < 0:
    #         raise ValidationError("Цена не может быть отрицательной")
    #     return price


class MailingClientModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = MailingClient
        fields = ('status',)