from rest_framework import permissions
from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet
from .models import EpidemiologyCase, ContactTrace, Outbreak
from .serializers import EpidemiologyCaseSerializer, ContactTraceSerializer, OutbreakSerializer


class EpidemiologyCaseViewSet(SoftDeleteAuditModelViewSet):
    queryset = EpidemiologyCase.objects.all()
    serializer_class = EpidemiologyCaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]


class ContactTraceViewSet(SoftDeleteAuditModelViewSet):
    queryset = ContactTrace.objects.all()
    serializer_class = ContactTraceSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]


class OutbreakViewSet(SoftDeleteAuditModelViewSet):
    queryset = Outbreak.objects.all()
    serializer_class = OutbreakSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]
