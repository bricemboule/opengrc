from django.db import models
from apps.core.models import SoftDeleteAuditModel


class Request(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="request_requests")
    code = models.CharField(max_length=80, unique=True)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class RequestItem(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="requestitem_requests")
    request = models.ForeignKey("Request", on_delete=models.CASCADE, null=False, blank=False, related_name="requestitem_request")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class RequestAssignment(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="requestassignment_requests")
    request = models.ForeignKey("Request", on_delete=models.CASCADE, null=False, blank=False, related_name="requestassignment_request")
    assignee = models.ForeignKey("people.Person", on_delete=models.SET_NULL, null=True, blank=True, related_name="requestassignment_assignee")
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)
