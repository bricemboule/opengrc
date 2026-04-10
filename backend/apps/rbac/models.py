from django.db import models
from django.contrib.auth.models import Permission
from apps.core.models import SoftDeleteAuditModel

class Role(SoftDeleteAuditModel):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, blank=True, related_name="custom_roles")

    def __str__(self):
        return self.name
