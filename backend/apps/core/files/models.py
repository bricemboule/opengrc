from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.core.models import SoftDeleteAuditModel


class Attachment(SoftDeleteAuditModel):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="attachments/%Y/%m/")
    mime_type = models.CharField(max_length=120, blank=True)
    size = models.PositiveIntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name
