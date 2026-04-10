from rest_framework import permissions
from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet
from .models import MissingPerson, MissingPersonReport
from .serializers import MissingPersonSerializer, MissingPersonReportSerializer


class MissingPersonViewSet(SoftDeleteAuditModelViewSet):
    queryset = MissingPerson.objects.all()
    serializer_class = MissingPersonSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]


class MissingPersonReportViewSet(SoftDeleteAuditModelViewSet):
    queryset = MissingPersonReport.objects.all()
    serializer_class = MissingPersonReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]
