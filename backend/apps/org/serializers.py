from rest_framework import serializers
from apps.core.serializers import AuditFieldsSerializerMixin
from .models import Facility, Organization, Site

class OrganizationSerializer(AuditFieldsSerializerMixin):
    class Meta:
        model = Organization
        fields = "__all__"


class SiteSerializer(AuditFieldsSerializerMixin):
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = Site
        fields = "__all__"


class FacilitySerializer(AuditFieldsSerializerMixin):
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    site_name = serializers.CharField(source="site.name", read_only=True)

    class Meta:
        model = Facility
        fields = "__all__"
