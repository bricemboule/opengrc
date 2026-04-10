from django.contrib import admin
from .models import Patient, Referral


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    search_fields = ("id",)


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    search_fields = ("id",)
