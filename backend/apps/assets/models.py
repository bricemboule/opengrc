from django.db import models
from apps.core.models import SoftDeleteAuditModel


class AssetType(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="assettype_assets")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class Asset(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="asset_assets")
    asset_type = models.ForeignKey("AssetType", on_delete=models.CASCADE, null=False, blank=False, related_name="asset_asset_type")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class Assignment(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="assignment_assets")
    asset = models.ForeignKey("Asset", on_delete=models.CASCADE, null=False, blank=False, related_name="assignment_asset")
    assignee = models.ForeignKey("people.Person", on_delete=models.SET_NULL, null=True, blank=True, related_name="assignment_assignee")
    assigned_to_name = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)
