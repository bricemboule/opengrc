from django.contrib import admin
from .models import Hospital, FacilityStatus


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    search_fields = ("id",)


@admin.register(FacilityStatus)
class FacilityStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    search_fields = ("id",)
