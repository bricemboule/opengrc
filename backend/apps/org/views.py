from django.core.cache import cache
from rest_framework.decorators import action
from apps.core.exports import export_as_csv
from apps.core.excel import export_as_excel
from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet
from .models import Facility, Organization, Site
from .serializers import FacilitySerializer, OrganizationSerializer, SiteSerializer
from .permissions import FacilityPermission, OrganizationPermission, SitePermission
from .filters import OrganizationFilter

class OrganizationViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [OrganizationPermission]
    filterset_class = OrganizationFilter
    search_fields = ["name", "code", "email", "phone"]
    ordering_fields = ["id", "name", "created_at"]

    def _clear_dashboard_cache(self):
        cache.clear()

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self._clear_dashboard_cache()

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
    queryset = Site.objects.select_related("organization").all()
    serializer_class = SiteSerializer
    permission_classes = [SitePermission]
    search_fields = ["name", "code", "city", "address", "email", "phone"]
    ordering_fields = ["id", "name", "code", "city", "created_at"]


class FacilityViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Facility.objects.select_related("organization", "site").all()
    serializer_class = FacilitySerializer
    permission_classes = [FacilityPermission]
    search_fields = ["name", "code", "facility_type", "city", "address", "contact_person"]
    ordering_fields = ["id", "name", "code", "facility_type", "status", "created_at"]
