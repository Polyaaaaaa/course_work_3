from django.db import models
from config import settings


# Create your models here.
class MailingClient(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, verbose_name="ф.и.о")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    comment = models.TextField(verbose_name="комментарий")

    class Meta:
        verbose_name = "получатель рассылки"
        verbose_name_plural = "получатели рассылок"
        ordering = ["email", "full_name"]
        permissions = [
            ("can_unpublish_product", "Can unpublish product"),
            ("can_delete_product", "Can delete product"),
            ("view_all_products", "View all products"),
        ]

    def __str__(self):
        return self.email


class MessageManagement(models.Model):
    subject = models.CharField(max_length=150, verbose_name="тема письма")
    body = models.TextField(verbose_name="тело письма")

    class Meta:
        verbose_name = "получатель рассылки"
        verbose_name_plural = "получатели рассылок"
        ordering = ["subject"]
