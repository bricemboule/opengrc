from rest_framework import permissions
from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet
from .models import Victim, Identification
from .serializers import VictimSerializer, IdentificationSerializer


class VictimViewSet(SoftDeleteAuditModelViewSet):
    queryset = Victim.objects.all()
    serializer_class = VictimSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]


class IdentificationViewSet(SoftDeleteAuditModelViewSet):
    queryset = Identification.objects.all()
    serializer_class = IdentificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]
