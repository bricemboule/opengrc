from django.contrib import admin
from .models import Alert, CapMessage


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    search_fields = ("id",)


@admin.register(CapMessage)
class CapMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    search_fields = ("id",)
