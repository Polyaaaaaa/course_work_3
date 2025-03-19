from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import (
    DeleteView,
    ListView,
    TemplateView,
    CreateView,
    UpdateView,
    DetailView,
)

from config import settings
from mailing_management.forms import (
    MailingClientForm,
    MailingClientModeratorForm,
    MessageManagementForm,
    NewsletterModeratorForm,
)
from mailing_management.forms import NewsletterForm
from mailing_management.models import MailingClient, MessageManagement, Newsletter, NewsletterStatistics
from mailing_management.services import (
    ClientService,
    MessageService,
    NewsletterService,
    send_newsletter,
)


# Create your views here.
class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MailingClient
    template_name = "mailing_management/client_confirm_delete.html"
    success_url = reverse_lazy("mailing_management:home")

    def test_func(self):
        client = self.get_object()
        return self.request.user == client.owner or self.request.user.has_perm(
            "can_delete_client"
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
    template_name = "mailing_management/client_form.html"
    success_url = reverse_lazy("mailing_management:home")

    def form_valid(self, form):
        if not self.request.user.has_perm("can_create_client"):
            raise PermissionDenied("У вас нет прав для создания клиента.")
        form.instance.owner = self.request.user  # Автоматически заполняем владельца
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MailingClient
    form_class = MailingClientForm
    template_name = "mailing_management/client_form.html"

    def test_func(self):
        client = self.get_object()
        # Разрешаем редактировать только владельцу или модератору
        return self.request.user == client.owner or self.request.user.has_perm(
            "can_edit_client"
        )

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
        raise PermissionDenied(
            "Извините, но вы не обладаете достаточным количеством прав."
        )

    def form_valid(self, form):
        # Проверяем, является ли пользователь модератором
        if self.request.user.has_perm("mailing_management.can_unpublish_client"):
            return super().form_valid(form)
        # Если пользователь не модератор, удаляем поле 'status' из данных формы
        form.cleaned_data.pop("status", None)
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = MailingClient
    template_name = "mailing_management/client_list.html"
    context_object_name = "clients"

    @method_decorator(cache_page(60 * 15))  # Кешируем страницу на 15 минут
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset  # Менеджеры могут видеть все
        return queryset.filter(owner=self.request.user)  # Пользователи видят только свои


class ClientDetailView(DetailView):
    model = MailingClient
    template_name = "mailing_management/client_detail.html"
    context_object_name = "client"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_id = self.object.id
        client_list = cache.get(f'client_list_{client_id}')

        if not client_list:
            client_list = ClientService.get_client_list(client_id)
            cache.set(f'client_list_{client_id}', client_list, timeout=60 * 15)  # Кешируем на 15 минут

        context["client_list"] = client_list
        return context


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MessageManagement
    template_name = "mailing_management/message_confirm_delete.html"
    success_url = reverse_lazy("mailing_management:home")

    def test_func(self):
        # Проверяем, имеет ли пользователь право на удаление
        return self.request.user.has_perm("mailing_management.can_delete_message")

    def post(self, request, *args, **kwargs):
        # Проверяем права доступа
        if not self.test_func():
            return HttpResponseForbidden("У вас нет прав для удаления этого объекта.")

        # Если права доступа есть, продолжаем с удалением
        return super().post(request, *args, **kwargs)


class MessageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MessageManagement
    form_class = MessageManagementForm
    template_name = "mailing_management/message_form.html"
    success_url = reverse_lazy("mailing_management:home")

    def test_func(self):
        # Проверяем, имеет ли пользователь право на создание
        return self.request.user.has_perm("mailing_management.can_create_message")

    def form_valid(self, form):
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MessageManagement
    form_class = MessageManagementForm
    template_name = "mailing_management/message_form.html"

    def get_success_url(self):
        return reverse(
            "mailing_management:message_detail", args=[self.kwargs.get("pk")]
        )

    def test_func(self):
        # Проверяем, имеет ли пользователь право на редактирование
        return self.request.user.has_perm("mailing_management.can_unpublish_message")

    def form_valid(self, form):
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = MessageManagement
    template_name = "mailing_management/message_list.html"
    context_object_name = "messages"

    def test_func(self):
        # Проверяем, имеет ли пользователь право на просмотр всех сообщений
        return self.request.user.has_perm("mailing_management.view_all_messages")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_delete"] = self.request.user.has_perm(
            "mailing_management.delete_message"
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class MessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = MessageManagement
    template_name = "mailing_management/message_detail.html"
    context_object_name = "message"

    def test_func(self):
        # Проверяем, имеет ли пользователь право на просмотр сообщения
        return self.request.user.has_perm("mailing_management.view_message")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message_id = self.object.id
        context["message_list"] = MessageService.get_message_list(message_id)
        return context


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter
    template_name = "mailing_management/newsletter_list.html"
    context_object_name = "newsletters"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_delete"] = self.request.user.has_perm(
            "mailing_management.delete_newsletter"
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        # Проверка прав доступа
        if not (
            self.request.user.is_staff
            or self.request.user.has_perm("mailing_management.view_all_newsletters")
        ):
            queryset = queryset.filter(owner=self.request.user)

        return queryset


class NewsletterDetailView(DetailView):
    model = Newsletter
    template_name = (
        "mailing_management/newsletter_detail.html"  # Обновляем путь, если необходимо
    )
    context_object_name = "newsletter"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        newsletter_id = self.object.id
        context["newsletter_list"] = NewsletterService.get_newsletter_list(
            newsletter_id
        )
        return context


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = "mailing_management/newsletter_form.html"
    success_url = reverse_lazy("mailing_management:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Newsletter
    template_name = "mailing_management/newsletter_form.html"

    def get_success_url(self):
        # return reverse_lazy("mailing_management:newsletter_list", args=[self.kwargs.get("pk")])
        return reverse_lazy("mailing_management:newsletter_list")

    def get_form_class(self):
        user = self.request.user
        # Если пользователь - владелец рассылки
        if user == self.get_object().owner:
            return NewsletterForm
        # Если пользователь - модератор
        if user.has_perm("mailing_management.can_unpublish_newsletter"):
            return NewsletterModeratorForm
        raise PermissionDenied(
            "Извините, но вы не обладаете достаточным количеством прав."
        )

    def test_func(self):
        # Получаем объект рассылки
        newsletter = self.get_object()
        # Можно редактировать рассылку, если пользователь - владелец или модератор
        return self.request.user == newsletter.owner or self.request.user.has_perm(
            "mailing_management.can_unpublish_newsletter"
        )

    def form_valid(self, form):
        # Проверяем, является ли пользователь модератором
        if self.request.user.has_perm("mailing_management.can_unpublish_newsletter"):
            return super().form_valid(form)
        # Если пользователь не модератор, удаляем поле 'status' из данных формы
        form.cleaned_data.pop("status", None)
        return super().form_valid(form)


class NewsletterDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Newsletter
    template_name = "mailing_management/newsletter_confirm_delete.html"
    success_url = reverse_lazy("mailing_management:newsletter_list")

    def test_func(self):
        # Проверяем, является ли пользователь владельцем рассылки или имеет ли он право на удаление
        return (
            self.request.user == self.get_object().owner
            or self.request.user.has_perm("mailing_management.can_delete_newsletter")
        )

    def post(self, request, *args, **kwargs):
        # Проверяем права доступа
        if not self.test_func():
            return HttpResponseForbidden("У вас нет прав для удаления этой рассылки.")

        # Если права доступа есть, продолжаем с удалением
        return super().post(request, *args, **kwargs)


class SendNewsletterView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "mailing_management.can_send_newsletter"

    def get(self, request, *args, **kwargs):
        newsletter_id = kwargs.get("pk")
        newsletter = get_object_or_404(Newsletter, id=newsletter_id)

        # Отправляем рассылку
        send_newsletter(newsletter)

        return redirect("mailing_management:newsletter_detail", pk=newsletter_id)


class HomeView(ListView):
    model = MailingClient  # Используем Client как основную модель для ListView
    template_name = "mailing_management/home.html"
    context_object_name = "clients"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_newsletters"] = Newsletter.objects.count()
        context["active_newsletters"] = Newsletter.objects.filter(
            status="Запущена"
        ).count()
        context["unique_recipients"] = (
            MailingClient.objects.values("email").distinct().count()
        )
        return context


class ContactsView(TemplateView):
    template_name = "mailing_management/contacts.html"


class SendMailAndUpdateStatisticsView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Логика отправки письма
        user = request.user
        subject = 'Тема письма'
        message = 'Текст сообщения'
        recipient_list = ['recipient@example.com']

        try:
            send_mail(subject, message, 'from@example.com', recipient_list)
            success = True
        except Exception as e:
            success = False

        # Обновляем статистику
        stats, created = NewsletterStatistics.objects.get_or_create(user=user)
        stats.update_statistics(success)

        # Возвращаем ответ с результатом
        return render(request, 'mailing_management/mail_sent.html', {'success': success})


class BlockUserView(LoginRequiredMixin, UserPassesTestMixin, View):
    permission_required = 'can_block_user'

    def test_func(self):
        # Проверяем, является ли пользователь администратором или менеджером
        return self.request.user.is_staff or self.request.user.has_perm("can_block_user")

    # Ваш код для блокировки пользователя

