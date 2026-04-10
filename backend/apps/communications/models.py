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
