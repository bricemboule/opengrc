from django.db import models
from apps.core.models import SoftDeleteAuditModel


class Event(SoftDeleteAuditModel):
    code = models.CharField(max_length=80, unique=True)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="active")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class Scenario(SoftDeleteAuditModel):
    event = models.ForeignKey("Event", on_delete=models.CASCADE, null=False, blank=False, related_name="scenario_event")
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class EventResource(SoftDeleteAuditModel):
    event = models.ForeignKey("Event", on_delete=models.CASCADE, null=False, blank=False, related_name="eventresource_event")
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)
