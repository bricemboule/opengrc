from django.conf import settings
from django.db import models

from apps.core.models import SoftDeleteAuditModel
from apps.org.models import Organization


class Message(SoftDeleteAuditModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="messages")
    channel = models.CharField(max_length=50, default="email")
    recipient = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.recipient


class Notification(SoftDeleteAuditModel):
    class EmailStatus(models.TextChoices):
        NOT_REQUESTED = "not_requested", "Not requested"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="notifications")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    source = models.CharField(max_length=80, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    email_status = models.CharField(max_length=20, choices=EmailStatus.choices, default=EmailStatus.NOT_REQUESTED)
    emailed_at = models.DateTimeField(null=True, blank=True)
    email_error = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return self.title or self.message[:80]
