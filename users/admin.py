from django.contrib import admin

# Register your models here.
from .models import CustomUser  # Импортируйте свою модель


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "phone_number",
        "avatar",
    )
    list_filter = ("email",)
