from django.contrib import admin
from .audit_models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("id", "model_name", "object_id", "action", "user", "created_at")
    search_fields = ("model_name", "object_id", "object_repr")
    list_filter = ("action", "model_name", "created_at")
