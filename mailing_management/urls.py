# catalog/urls.py
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from mailing_management.views import (
    HomeView,
    ClientDeleteView,
    ContactsView,
    ClientCreateView,
    ClientUpdateView,
    ClientDetailView,
    MessageListView,
    MessageDetailView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    NewsletterListView,
    NewsletterDetailView,
    NewsletterCreateView,
    NewsletterUpdateView,
    NewsletterDeleteView,
)
from mailing_management.views import ClientListView

app_name = "products"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),  # URL для главной страницы
    path(
        "contacts/", ContactsView.as_view(), name="contacts"
    ),  # URL для страницы контактов
    path(
        "clients/<int:pk>/", ClientDetailView.as_view(), name="client_detail"
    ),  # URL для деталей продукта
    path("client_create/", ClientCreateView.as_view(), name="client_form"),
    path(
        "clients/<int:pk>/update/", ClientUpdateView.as_view(), name="client_update"
    ),  # URL для обновления продукта
    path("clients_list/", ClientListView.as_view(), name="client_list"),
    path("clients/<int:pk>/delete/", ClientDeleteView.as_view(), name="delete_client"),
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("messages/create/", MessageCreateView.as_view(), name="message_create"),
    path(
        "messages/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("newsletters/", NewsletterListView.as_view(), name="newsletter_list"),
    path(
        "newsletters/<int:pk>/",
        NewsletterDetailView.as_view(),
        name="newsletter_detail",
    ),
    path(
        "newsletters/create/", NewsletterCreateView.as_view(), name="newsletter_create"
    ),
    path(
        "newsletters/<int:pk>/update/",
        NewsletterUpdateView.as_view(),
        name="newsletter_update",
    ),
    path(
        "newsletters/<int:pk>/delete/",
        NewsletterDeleteView.as_view(),
        name="newsletter_delete",
    ),
]
