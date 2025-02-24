from django.db import models
from config import settings
from users.models import CustomUser


# Create your models here.
class MailingClient(models.Model):
    owner = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="added_clients",
        verbose_name="Владелец (кто добавил)"
    )
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="mailing_clients",
        verbose_name="Пользователь (если зарегистрирован)"
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, verbose_name="ф.и.о")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    comment = models.TextField(verbose_name="комментарий")

    class Meta:
        verbose_name = "получатель рассылки"
        verbose_name_plural = "получатели рассылок"
        ordering = ["email", "full_name"]
        permissions = [
            ("can_unpublish_client", "Can unpublish client"),
            ("can_delete_client", "Can delete client"),
            ("view_all_clients", "View all clients"),
            ("can_create_client", "Can create a client"),
            ("can_edit_client", "Can edit a client"),
        ]

    def __str__(self):
        return self.email


class MessageManagement(models.Model):
    subject = models.CharField(max_length=150, verbose_name="тема письма")
    body = models.TextField(verbose_name="тело письма")

    class Meta:
        verbose_name = "письмо"
        verbose_name_plural = "письма"
        ordering = ["subject"]


class Newsletter(models.Model):
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="newsletters",
        null=True,
        blank=True,
    )  # Разрешаем NULL
    NEWSLETTER_STATUS_CHOICES = [
        ("created", "Создана"),
        ("started", "Запущена"),
        ("finished", "Завершена"),
    ]

    beginning_date = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Дата и время первой отправки"
    )
    end_date = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Дата и время окончания отправки"
    )
    status = models.CharField(
        max_length=12,
        choices=NEWSLETTER_STATUS_CHOICES,
        default="created",
        verbose_name="Статус публикации",
    )
    message = models.ForeignKey(
        MessageManagement, on_delete=models.CASCADE, verbose_name="Сообщение "
    )
    clients = models.ManyToManyField(MailingClient, verbose_name="Получатели ")

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        ordering = ["message"]

        permissions = [
            ("can_unpublish_newsletter", "Can unpublish newsletter"),
            ("can_delete_newsletter", "Can delete newsletter"),
            ("view_all_newsletters", "View all newsletters"),
        ]


class NewsletterAttempt(models.Model):
    ATTEMPT_STATUS_CHOICES = [
        ("successful", "Успешно"),
        ("failed", "Не успешно"),
    ]

    attempt_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время попытки"
    )
    status = models.CharField(
        max_length=12, choices=ATTEMPT_STATUS_CHOICES, verbose_name="Статус попытки"
    )
    server_response = models.TextField(
        verbose_name="Ответ почтового сервера", blank=True, null=True
    )
    newsletter = models.ForeignKey(
        "Newsletter",
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="Рассылка",
    )

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылок"
        ordering = ["-attempt_date"]

    def __str__(self):
        return f"Попытка {self.id} для рассылки {self.newsletter.id}"


class NewsletterStatistics(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_sent = models.IntegerField(default=0)  # Общее количество отправленных сообщений
    successful_attempts = models.IntegerField(default=0)  # Количество успешных попыток
    failed_attempts = models.IntegerField(default=0)  # Количество неуспешных попыток
    last_update = models.DateTimeField(auto_now=True)  # Время последнего обновления статистики

    def __str__(self):
        return f"Статистика для {self.user.username}"

    def update_statistics(self, success=True):
        """
        Обновляет статистику в зависимости от результата отправки сообщения.
        """
        if success:
            self.successful_attempts += 1
        else:
            self.failed_attempts += 1
        self.total_sent += 1
        self.save()

