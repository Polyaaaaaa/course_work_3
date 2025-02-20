from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, ListView, TemplateView, CreateView, UpdateView, DetailView

from mailing_management.forms import MailingClientForm, MailingClientModeratorForm, MessageManagementForm, \
    NewsletterModeratorForm
from mailing_management.forms import NewsletterForm
from mailing_management.models import MailingClient, MessageManagement, Newsletter
from mailing_management.services import ClientService, MessageService, NewsletterService


# Create your views here.
class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MailingClient
    template_name = "mailing_management/client_confirm_delete.html"
    context_object_name = "moderator"
    success_url = reverse_lazy("mailing_management:home")

    def test_func(self):
        # Проверяем, является ли пользователь владельцем продукта или имеет ли он право на удаление
        return self.request.user.has_perm(
            "moderator.can_delete_client"
        )

    def post(self, request, *args, **kwargs):
        # Проверяем права доступа
        if not self.test_func():
            return HttpResponseForbidden("У вас нет прав для удаления этого продукта.")

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
        return reverse_lazy("mailing_management:home")


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
        if user.has_perm("mailing_management.can_unpublish_client"):
            return MailingClientModeratorForm
        raise PermissionDenied('Извините, но вы не обладаете достаточным количеством прав.')

    # def test_func(self):
    #     # Получаем объект продукта
    #     product = self.get_object()
    #     # Можно редактировать продукт, если пользователь - владелец или модератор
    #     return self.request.user == product.owner or self.request.user.has_perm("catalog.can_unpublish_product")

    def form_valid(self, form):
        # Проверяем, является ли пользователь модератором
        if self.request.user.has_perm("mailing_management.can_unpublish_client"):
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
        client_id = self.object.id  # Используйте `id` вместо `client_id`
        context['client_list'] = ClientService.get_client_list(client_id)
        return context

    def get_success_url(self):
        return reverse("mailing_management:client_detail", args=[self.object.pk])


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MessageManagement
    template_name = "mailing_management/message_confirm_delete.html"
    success_url = reverse_lazy("mailing_management:home")

    def test_func(self):
        # Проверяем, имеет ли пользователь право на удаление
        return self.request.user.has_perm("moderator.can_delete_client")

    def post(self, request, *args, **kwargs):
        # Проверяем права доступа
        if not self.test_func():
            return HttpResponseForbidden("У вас нет прав для удаления этого объекта.")

        # Если права доступа есть, продолжаем с удалением
        return super().post(request, *args, **kwargs)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = MessageManagement
    form_class = MessageManagementForm
    template_name = 'mailing_management/message_form.html'
    success_url = reverse_lazy("mailing_management:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("mailing_management:message_detail.html", args=[self.object.pk])


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MessageManagement
    form_class = MailingClientForm
    template_name = 'mailing_management/message_form.html'

    def get_success_url(self):
        return reverse("mailing_management:message_detail", args=[self.kwargs.get("pk")])

    def get_form_class(self):
        user = self.request.user
        # Если пользователь - владелец продукта
        if user == self.get_object().owner:
            return MailingClientForm
        # Если пользователь - модератор
        if user.has_perm("mailing_management.can_unpublish_client"):
            return MailingClientModeratorForm
        raise PermissionDenied('Извините, но вы не обладаете достаточным количеством прав.')

    # def test_func(self):
    #     # Получаем объект продукта
    #     product = self.get_object()
    #     # Можно редактировать продукт, если пользователь - владелец или модератор
    #     return self.request.user == product.owner or self.request.user.has_perm("catalog.can_unpublish_product")

    def form_valid(self, form):
        # Проверяем, является ли пользователь модератором
        if self.request.user.has_perm("mailing_management.can_unpublish_client"):
            return super().form_valid(form)
        # Если пользователь не модератор, удаляем поле 'status' из данных формы
        form.cleaned_data.pop('status', None)
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = MessageManagement
    template_name = "mailing_management/message_list.html"
    context_object_name = "messages"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_delete'] = self.request.user.has_perm('mailing_management.delete_message')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        # Проверка прав доступа
        if not (self.request.user.is_staff or self.request.user.has_perm("mailing_management.view_all_messages")):
            queryset = queryset.filter(owner=self.request.user)

        return queryset


class MessageDetailView(DetailView):
    model = MessageManagement
    template_name = 'mailing_management/message_detail.html'
    context_object_name = 'message'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message_id = self.object.id
        context['message_list'] = MessageService.get_message_list(message_id)
        return context


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter
    template_name = 'newsletter_list.html'
    context_object_name = 'newsletters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_delete'] = self.request.user.has_perm('mailing_management.delete_newsletter')
        return context

    class NewsletterListView(LoginRequiredMixin, ListView):
        model = Newsletter
        template_name = "mailing_management/newsletter_list.html"
        context_object_name = "newsletters"

        def get_queryset(self):
            queryset = super().get_queryset()

            # Пример фильтрации по статусу или другим полям
            queryset = queryset.filter(status='created')

            return queryset


class NewsletterDetailView(DetailView):
    model = Newsletter
    template_name = 'newsletter_detail.html'
    context_object_name = 'newsletter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        newsletter_id = self.object.id  # Используйте `id` вместо `client_id`
        context['newsletter_list'] = NewsletterService.get_newsletter_list(newsletter_id)
        return context

    def get_success_url(self):
        return reverse("mailing_management:newsletter_detail", args=[self.object.pk])


class NewsletterCreateView(CreateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'newsletter_form.html'
    # success_url = reverse_lazy('newsletter_list')  # Перенаправление после успешного сохранения
    success_url = reverse_lazy("mailing_management:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("mailing_management:home")


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'newsletter_form.html'
    success_url = reverse_lazy('newsletter_list')  # Перенаправление после успешного обновления

    def get_success_url(self):
        return reverse("mailing_management:newsletter_detail", args=[self.kwargs.get("pk")])

    def get_form_class(self):
        user = self.request.user
        # Если пользователь - владелец продукта
        if user == self.get_object().owner:
            return NewsletterForm
        # Если пользователь - модератор
        if user.has_perm("mailing_management.can_unpublish_newsletter"):
            return NewsletterModeratorForm
        raise PermissionDenied('Извините, но вы не обладаете достаточным количеством прав.')

    # def test_func(self):
    #     # Получаем объект продукта
    #     product = self.get_object()
    #     # Можно редактировать продукт, если пользователь - владелец или модератор
    #     return self.request.user == product.owner or self.request.user.has_perm("catalog.can_unpublish_product")


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    template_name = 'newsletter_confirm_delete.html'
    success_url = reverse_lazy('mailing_management:newsletter_list')  # Перенаправление после успешного удаления

    def test_func(self):
        # Проверяем, является ли пользователь владельцем рассылки или имеет ли он право на удаление
        return self.request.user.has_perm(
            "moderator.can_delete_newsletter"
        )

    def post(self, request, *args, **kwargs):
        # Проверяем права доступа
        if not self.test_func():
            return HttpResponseForbidden("У вас нет прав для удаления этой рассылки продукта.")

        # Если права доступа есть, продолжаем с удалением
        return super().post(request, *args, **kwargs)


class HomeView(ListView):
    model = MailingClient
    template_name = "mailing_management/home.html"


class ContactsView(TemplateView):
    template_name = "mailing_management/contacts.html"



