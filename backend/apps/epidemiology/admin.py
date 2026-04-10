from django.contrib import admin
from .models import EpidemiologyCase, ContactTrace, Outbreak


@admin.register(EpidemiologyCase)
class EpidemiologyCaseAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    search_fields = ("id",)


@admin.register(ContactTrace)
class ContactTraceAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    search_fields = ("id",)


@admin.register(Outbreak)
class OutbreakAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    search_fields = ("id",)
