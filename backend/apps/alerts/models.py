from django.db import models
from apps.core.models import SoftDeleteAuditModel


class Alert(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="alert_alerts")
    code = models.CharField(max_length=80, unique=True)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="active")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class CapMessage(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="capmessage_alerts")
    alert = models.ForeignKey("Alert", on_delete=models.CASCADE, null=False, blank=False, related_name="capmessage_alert")
    identifier = models.CharField(max_length=80, unique=True)
    headline = models.CharField(max_length=255)
    scope = models.CharField(max_length=100, default="public")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)
