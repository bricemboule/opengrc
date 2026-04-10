from django.db import models
from apps.core.models import SoftDeleteAuditModel


class Client(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="client_case_management")
    person = models.ForeignKey("people.Person", on_delete=models.CASCADE, null=False, blank=False, related_name="client_person")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class CaseFile(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="casefile_case_management")
    client = models.ForeignKey("Client", on_delete=models.CASCADE, null=False, blank=False, related_name="casefile_client")
    case_number = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class CaseEvent(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="caseevent_case_management")
    case_file = models.ForeignKey("CaseFile", on_delete=models.CASCADE, null=False, blank=False, related_name="caseevent_case_file")
    event_type = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)
