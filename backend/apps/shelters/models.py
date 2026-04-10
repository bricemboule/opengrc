from django.db import models
from apps.core.models import SoftDeleteAuditModel


class Shelter(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="shelter_shelters")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="active")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class Occupancy(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="occupancy_shelters")
    shelter = models.ForeignKey("Shelter", on_delete=models.CASCADE, null=False, blank=False, related_name="occupancy_shelter")
    name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class Checkin(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="checkin_shelters")
    shelter = models.ForeignKey("Shelter", on_delete=models.CASCADE, null=False, blank=False, related_name="checkin_shelter")
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)
