from rest_framework import permissions
from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet
from .models import Department, JobTitle, Staff
from .serializers import DepartmentSerializer, JobTitleSerializer, StaffSerializer


class DepartmentViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]


class JobTitleViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]


class StaffViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]
