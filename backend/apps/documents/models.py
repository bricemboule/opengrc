from django.db import models
from apps.core.models import SoftDeleteAuditModel


class Document(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="document_documents")
    code = models.CharField(max_length=80, unique=True)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class FileAttachment(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="fileattachment_documents")
    document = models.ForeignKey("Document", on_delete=models.CASCADE, null=False, blank=False, related_name="fileattachment_document")
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)
