from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("id", "email", "username", "full_name", "organization", "is_staff", "is_active")
    search_fields = ("email", "username", "full_name")
    ordering = ("-id",)
    fieldsets = UserAdmin.fieldsets + (
        ("Informations supplémentaires", {"fields": ("full_name", "phone", "organization", "roles", "is_verified")}),
    )
