from django.db import models
from django.core.exceptions import ValidationError
from apps.core.models import SoftDeleteAuditModel
from apps.org.models import Organization

class Person(SoftDeleteAuditModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="people")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Contact(SoftDeleteAuditModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="contacts")
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="contacts")
    contact_type = models.CharField(max_length=32, default="SMS")
    value = models.CharField(max_length=255)
    label = models.CharField(max_length=255, blank=True)
    priority = models.PositiveSmallIntegerField(default=1)
    is_primary = models.BooleanField(default=False)
    access_level = models.CharField(max_length=32, default="private")
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ["priority", "-id"]

    def __str__(self):
        return f"{self.person} - {self.contact_type}"

    def clean(self):
        if self.person_id and self.organization_id and self.person.organization_id != self.organization_id:
            raise ValidationError({"person": "La personne doit appartenir a la meme organisation."})


class Identity(SoftDeleteAuditModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="identities")
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="identities")
    document_type = models.CharField(max_length=50, default="national_id")
    description = models.CharField(max_length=255, blank=True)
    document_number = models.CharField(max_length=120, blank=True)
    valid_from = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    issued_country = models.CharField(max_length=4, blank=True)
    issued_place = models.CharField(max_length=255, blank=True)
    issuing_authority = models.CharField(max_length=255, blank=True)
    is_system_generated = models.BooleanField(default=False)
    is_invalid = models.BooleanField(default=False)
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.person} - {self.document_type}"

    def clean(self):
        if self.person_id and self.organization_id and self.person.organization_id != self.organization_id:
            raise ValidationError({"person": "La personne doit appartenir a la meme organisation."})
        if self.valid_from and self.valid_until and self.valid_until < self.valid_from:
            raise ValidationError({"valid_until": "La date de fin de validite doit etre posterieure a la date de debut."})
