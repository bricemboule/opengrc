from django.apps import AppConfig


class IncidentManagementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.incident_management"

    def ready(self):
        from . import signals  # noqa: F401
