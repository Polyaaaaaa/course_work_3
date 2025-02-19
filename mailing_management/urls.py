# catalog/urls.py
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from mailing_management.views import HomeView, ClientDeleteView, ContactsView, ClientCreateView, ClientUpdateView, \
    ClientListView

app_name = "products"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),  # URL для главной страницы
    path(
        "contacts/", ContactsView.as_view(), name="contacts"
    ),  # URL для страницы контактов
    # path(
    #     "products/<int:pk>/", ClientDetailView.as_view(), name="client_detail"
    # ),  # URL для деталей продукта
    path("client_create/", ClientCreateView.as_view(), name="client_form"),
    path("products/<int:pk>/update/", ClientUpdateView.as_view(), name="client_update"), # URL для обновления продукта
    path('products/<int:pk>/unpublish/', ClientListView.as_view(), name='unpublish_client'),
    path('products/<int:pk>/delete/', ClientDeleteView.as_view(), name='delete_client'),
]