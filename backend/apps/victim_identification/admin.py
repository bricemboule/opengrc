from django.contrib import admin
from .models import Victim, Identification


@admin.register(Victim)
class VictimAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    search_fields = ("id",)


@admin.register(Identification)
class IdentificationAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    search_fields = ("id",)
