from django.db import models
from apps.core.models import SoftDeleteAuditModel


class Patient(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="patient_patients")
    person = models.ForeignKey("people.Person", on_delete=models.CASCADE, null=False, blank=False, related_name="patient_person")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="active")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class Referral(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="referral_patients")
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE, null=False, blank=False, related_name="referral_patient")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)
