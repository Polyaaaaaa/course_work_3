from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView

from mailing_management.models import MailingClient


# Create your views here.
class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MailingClient
    template_name = "mailing_management/product_confirm_delete.html"
    context_object_name = "moderator"
    success_url = reverse_lazy("clients:home")

    # def test_func(self):
    #     client = self.get_object()
    #     # Проверяем, является ли пользователь владельцем продукта или имеет ли он право на удаление
    #     return self.request.user == client.owner or self.request.user.has_perm(
    #         "moderator.can_delete_client"
    #     )

    def post(self, request, *args, **kwargs):
        client = self.get_object()
        # Проверяем права доступа
        # if not self.test_func():
        #     return HttpResponseForbidden("У вас нет прав для удаления этого продукта.")

        # Если права доступа есть, продолжаем с удалением
        return super().post(request, *args, **kwargs)


class HomeView(ListView):
    model = MailingClient
    template_name = "mailing_management/home.html"
