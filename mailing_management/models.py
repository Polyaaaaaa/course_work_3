from django.db import models
from config import settings
from users.models import CustomUser


# Create your models here.
class MailingClient(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, verbose_name="ф.и.о")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    comment = models.TextField(verbose_name="комментарий")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = "получатель рассылки"
        verbose_name_plural = "получатели рассылок"
        ordering = ["email", "full_name"]
        permissions = [
            ("can_unpublish_client", "Can unpublish client"),
            ("can_delete_client", "Can delete client"),
            ("view_all_clients", "View all clients"),
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
    NEWSLETTER_STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('finished', 'Завершена'),
    ]

    beginning_date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Дата и время первой отправки")
    end_date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Дата и время окончания отправки")
    status = models.CharField(
        max_length=12,
        choices=NEWSLETTER_STATUS_CHOICES,
        default='created',
        verbose_name="Статус публикации"
    )
    message = models.ForeignKey(MessageManagement, on_delete=models.CASCADE, verbose_name="Сообщение ")
    clients = models.ManyToManyField(MailingClient, verbose_name="Получатели ")
