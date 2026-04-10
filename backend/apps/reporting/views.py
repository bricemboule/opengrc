from rest_framework import permissions
from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet
from .models import Report, Dashboard, Metric
from .serializers import ReportSerializer, DashboardSerializer, MetricSerializer


class ReportViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]


class DashboardViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]


class MetricViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]
