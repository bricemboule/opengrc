from django.contrib import admin
from .models import Facility, FacilityType, OfficeType, Organization, OrganizationType, Site

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "organization_type", "email", "is_active")
    search_fields = ("name", "code", "email")


@admin.register(OrganizationType)
class OrganizationTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "code", "name", "status")
    search_fields = ("code", "name")


@admin.register(OfficeType)
class OfficeTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "code", "name", "status")
    search_fields = ("code", "name")


@admin.register(FacilityType)
class FacilityTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "code", "name", "status")
    search_fields = ("code", "name")


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "name", "office_type", "city", "status")
    search_fields = ("name", "code", "city", "address")


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "name", "facility_type_ref", "city", "status")
    search_fields = ("name", "code", "city", "address")
