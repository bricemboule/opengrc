from rest_framework import permissions
from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet
from .models import AssetType, Asset, Assignment
from .serializers import AssetTypeSerializer, AssetSerializer, AssignmentSerializer


class AssetTypeViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = AssetType.objects.select_related("organization").all()
    serializer_class = AssetTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]


class AssetViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Asset.objects.select_related("organization", "asset_type").all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]


class AssignmentViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Assignment.objects.select_related("organization", "asset", "assignee").all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]
