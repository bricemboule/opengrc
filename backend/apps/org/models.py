from django.db import models
from apps.core.models import SoftDeleteAuditModel


class OrganizationType(SoftDeleteAuditModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE, related_name="organization_types")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, default="active")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class OfficeType(SoftDeleteAuditModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE, related_name="office_types")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, default="active")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class FacilityType(SoftDeleteAuditModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE, related_name="facility_types")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, default="active")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Organization(SoftDeleteAuditModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=80, unique=True)
    organization_type = models.ForeignKey(OrganizationType, on_delete=models.SET_NULL, null=True, blank=True, related_name="organizations")
    description = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Site(SoftDeleteAuditModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="sites")
    office_type = models.ForeignKey(OfficeType, on_delete=models.SET_NULL, null=True, blank=True, related_name="sites")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=80, unique=True)
    site_type = models.CharField(max_length=50, default="office")
    city = models.CharField(max_length=120, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    alternate_phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    fax = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, default="active")
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Facility(SoftDeleteAuditModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="facilities")
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True, related_name="facilities")
    facility_type_ref = models.ForeignKey(FacilityType, on_delete=models.SET_NULL, null=True, blank=True, related_name="facilities")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=80, unique=True)
    facility_type = models.CharField(max_length=80, default="general")
    status = models.CharField(max_length=50, default="active")
    city = models.CharField(max_length=120, blank=True)
    address = models.CharField(max_length=255, blank=True)
    contact_person = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    opening_times = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name
