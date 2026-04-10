from rest_framework import permissions
from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet
from .models import BudgetPlan, BudgetLine
from .serializers import BudgetPlanSerializer, BudgetLineSerializer


class BudgetPlanViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = BudgetPlan.objects.all()
    serializer_class = BudgetPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]


class BudgetLineViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = BudgetLine.objects.all()
    serializer_class = BudgetLineSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]
