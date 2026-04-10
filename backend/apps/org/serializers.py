from rest_framework import serializers
from apps.core.serializers import AuditFieldsSerializerMixin
from .models import Facility, FacilityType, OfficeType, Organization, OrganizationType, Site

class OrganizationSerializer(AuditFieldsSerializerMixin):
    organization_type_name = serializers.CharField(source="organization_type.name", read_only=True)

    class Meta:
        model = Organization
        fields = "__all__"


class SiteSerializer(AuditFieldsSerializerMixin):
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    office_type_name = serializers.CharField(source="office_type.name", read_only=True)

    class Meta:
        model = Site
        fields = "__all__"


class FacilitySerializer(AuditFieldsSerializerMixin):
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    site_name = serializers.CharField(source="site.name", read_only=True)
    facility_type_name = serializers.SerializerMethodField()

    class Meta:
        model = Facility
        fields = "__all__"

    def get_facility_type_name(self, obj):
        return obj.facility_type_ref.name if obj.facility_type_ref else obj.facility_type


class OrganizationTypeSerializer(AuditFieldsSerializerMixin):
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = OrganizationType
        fields = "__all__"


class OfficeTypeSerializer(AuditFieldsSerializerMixin):
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = OfficeType
        fields = "__all__"


class FacilityTypeSerializer(AuditFieldsSerializerMixin):
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = FacilityType
        fields = "__all__"
