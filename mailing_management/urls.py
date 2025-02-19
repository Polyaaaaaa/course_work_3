# catalog/urls.py
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from mailing_management.views import HomeView, ClientDeleteView, ContactsView, ClientCreateView, ClientUpdateView, \
    ClientDetailView
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
    path("clients/<int:pk>/update/", ClientUpdateView.as_view(), name="client_update"), # URL для обновления продукта
    path('clients/<int:pk>/unpublish/', ClientListView.as_view(), name='unpublish_client'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='delete_client'),
]