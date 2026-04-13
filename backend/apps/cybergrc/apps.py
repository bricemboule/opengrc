from django.apps import AppConfig


class CybergrcConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.cybergrc"
    verbose_name = "Cyber GRC"

    def ready(self):
        from . import signals  # noqa: F401
