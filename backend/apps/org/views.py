from django.core.cache import cache
from rest_framework.decorators import action
from apps.core.exports import export_as_csv
from apps.core.excel import export_as_excel
from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet
from .models import Facility, FacilityType, OfficeType, Organization, OrganizationType, Site
from .serializers import (
    FacilitySerializer,
    FacilityTypeSerializer,
    OfficeTypeSerializer,
    OrganizationSerializer,
    OrganizationTypeSerializer,
    SiteSerializer,
)
from .permissions import (
    FacilityPermission,
    FacilityTypePermission,
    OfficeTypePermission,
    OrganizationPermission,
    OrganizationTypePermission,
    SitePermission,
)
from .filters import OrganizationFilter

class OrganizationViewSet(SoftDeleteAuditModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [OrganizationPermission]
    filterset_class = OrganizationFilter
    search_fields = ["name", "code", "email", "phone"]
    ordering_fields = ["id", "name", "created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset
        if not getattr(user, "organization_id", None):
            return queryset.none()
        return queryset.filter(id=user.organization_id)

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        instance = serializer.save(created_by=user, updated_by=user)
        self.log_action("create", instance)
        self._clear_dashboard_cache()

    def _clear_dashboard_cache(self):
        cache.clear()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self._clear_dashboard_cache()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self._clear_dashboard_cache()

    @action(detail=False, methods=["get"], url_path="export-csv")
    def export_csv(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        return export_as_csv(
            filename="organizations.csv",
            field_names=["ID", "Name", "Code", "Email", "Active"],
            queryset=queryset,
            row_builder=lambda obj: [obj.id, obj.name, obj.code, obj.email, "Yes" if obj.is_active else "No"],
        )

    @action(detail=False, methods=["get"], url_path="export-excel")
    def export_excel(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        return export_as_excel(
            filename="organizations.xlsx",
            headers=["ID", "Name", "Code", "Email", "Active"],
            queryset=queryset,
            row_builder=lambda obj: [obj.id, obj.name, obj.code, obj.email, "Yes" if obj.is_active else "No"],
            sheet_name="Organizations",
        )


class SiteViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Site.objects.select_related("organization", "office_type").all()
    serializer_class = SiteSerializer
    permission_classes = [SitePermission]
    search_fields = ["name", "code", "city", "address", "email", "phone", "office_type__name"]
    ordering_fields = ["id", "name", "code", "city", "created_at"]


class FacilityViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Facility.objects.select_related("organization", "site", "facility_type_ref").all()
    serializer_class = FacilitySerializer
    permission_classes = [FacilityPermission]
    search_fields = ["name", "code", "facility_type", "city", "address", "contact_person", "facility_type_ref__name"]
    ordering_fields = ["id", "name", "code", "facility_type", "status", "created_at"]


class OrganizationTypeViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = OrganizationType.objects.select_related("organization").all()
    serializer_class = OrganizationTypeSerializer
    permission_classes = [OrganizationTypePermission]
    search_fields = ["code", "name", "description", "status"]
    ordering_fields = ["id", "name", "code", "created_at"]


class OfficeTypeViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = OfficeType.objects.select_related("organization").all()
    serializer_class = OfficeTypeSerializer
    permission_classes = [OfficeTypePermission]
    search_fields = ["code", "name", "description", "status"]
    ordering_fields = ["id", "name", "code", "created_at"]


class FacilityTypeViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = FacilityType.objects.select_related("organization").all()
    serializer_class = FacilityTypeSerializer
    permission_classes = [FacilityTypePermission]
    search_fields = ["code", "name", "description", "status"]
    ordering_fields = ["id", "name", "code", "created_at"]
