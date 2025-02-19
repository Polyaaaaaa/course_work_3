from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, ListView, TemplateView, CreateView, UpdateView, DetailView

from mailing_management.forms import MailingClientForm, MailingClientModeratorForm
from mailing_management.models import MailingClient, MessageManagement
from mailing_management.services import ClientService


# Create your views here.
class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MailingClient
    template_name = "mailing_management/product_confirm_delete.html"
    context_object_name = "moderator"
    success_url = reverse_lazy("mailing_management:home")

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


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = MailingClient
    form_class = MailingClientForm
    template_name = 'mailing_management/client_form.html'
    success_url = reverse_lazy("mailing_management:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("mailing_management:client_detail.html", args=[self.object.pk])


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MailingClient
    form_class = MailingClientForm
    template_name = 'mailing_management/client_form.html'

    def get_success_url(self):
        return reverse("mailing_management:client_detail", args=[self.kwargs.get("pk")])

    def get_form_class(self):
        user = self.request.user
        # Если пользователь - владелец продукта
        if user == self.get_object().owner:
            return MailingClientForm
        # Если пользователь - модератор
        if user.has_perm("mailing_management.can_unpublish_product"):
            return MailingClientModeratorForm
        raise PermissionDenied('Извините, но вы не обладаете достаточным количеством прав.')

    # def test_func(self):
    #     # Получаем объект продукта
    #     product = self.get_object()
    #     # Можно редактировать продукт, если пользователь - владелец или модератор
    #     return self.request.user == product.owner or self.request.user.has_perm("catalog.can_unpublish_product")

    def form_valid(self, form):
        # Проверяем, является ли пользователь модератором
        if self.request.user.has_perm("mailing_management.can_unpublish_product"):
            return super().form_valid(form)
        # Если пользователь не модератор, удаляем поле 'status' из данных формы
        form.cleaned_data.pop('status', None)
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = MailingClient
    template_name = "mailing_management/client_list.html"
    context_object_name = "clients"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_delete'] = self.request.user.has_perm('mailing_management.delete_client')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        # Проверка прав доступа
        if not (self.request.user.is_staff or self.request.user.has_perm("mailing_management.view_all_clients")):
            queryset = queryset.filter(owner=self.request.user)

        return queryset


class ClientDetailView(DetailView):
    model = MailingClient
    template_name = 'mailing_management/client_detail.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.object.id
        context['product_list'] = ClientService.get_product_list(product_id)
        return context


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MessageManagement
    template_name = "mailing_management/message_confirm_delete.html"
    context_object_name = "moderator"
    success_url = reverse_lazy("mailing_management:home")

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


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = MessageManagement
    form_class = MailingClientForm
    template_name = 'mailing_management/client_form.html'
    success_url = reverse_lazy("mailing_management:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("mailing_management:client_detail.html", args=[self.object.pk])


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MailingClient
    form_class = MailingClientForm
    template_name = 'mailing_management/client_form.html'

    def get_success_url(self):
        return reverse("mailing_management:client_detail", args=[self.kwargs.get("pk")])

    def get_form_class(self):
        user = self.request.user
        # Если пользователь - владелец продукта
        if user == self.get_object().owner:
            return MailingClientForm
        # Если пользователь - модератор
        if user.has_perm("mailing_management.can_unpublish_product"):
            return MailingClientModeratorForm
        raise PermissionDenied('Извините, но вы не обладаете достаточным количеством прав.')

    # def test_func(self):
    #     # Получаем объект продукта
    #     product = self.get_object()
    #     # Можно редактировать продукт, если пользователь - владелец или модератор
    #     return self.request.user == product.owner or self.request.user.has_perm("catalog.can_unpublish_product")

    def form_valid(self, form):
        # Проверяем, является ли пользователь модератором
        if self.request.user.has_perm("mailing_management.can_unpublish_product"):
            return super().form_valid(form)
        # Если пользователь не модератор, удаляем поле 'status' из данных формы
        form.cleaned_data.pop('status', None)
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = MailingClient
    template_name = "mailing_management/client_list.html"
    context_object_name = "clients"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_delete'] = self.request.user.has_perm('mailing_management.delete_client')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        # Проверка прав доступа
        if not (self.request.user.is_staff or self.request.user.has_perm("mailing_management.view_all_clients")):
            queryset = queryset.filter(owner=self.request.user)

        return queryset


class MessageDetailView(DetailView):
    model = MailingClient
    template_name = 'mailing_management/client_detail.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.object.id
        context['product_list'] = ClientService.get_product_list(product_id)
        return context


class HomeView(ListView):
    model = MailingClient
    template_name = "mailing_management/home.html"


class ContactsView(TemplateView):
    template_name = "mailing_management/contacts.html"



