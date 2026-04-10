from django.db import models
from apps.core.models import SoftDeleteAuditModel


class MedicalRecord(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="medicalrecord_medical")
    patient = models.ForeignKey("patients.Patient", on_delete=models.CASCADE, null=False, blank=False, related_name="medicalrecord_patient")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class Consultation(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="consultation_medical")
    patient = models.ForeignKey("patients.Patient", on_delete=models.CASCADE, null=False, blank=False, related_name="consultation_patient")
    hospital = models.ForeignKey("health_facilities.Hospital", on_delete=models.SET_NULL, null=True, blank=True, related_name="consultation_hospital")
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)
