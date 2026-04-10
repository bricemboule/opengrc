from rest_framework import permissions
from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet
from .models import Volunteer, Skill, Availability
from .serializers import VolunteerSerializer, SkillSerializer, AvailabilitySerializer


class VolunteerViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]


class SkillViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]


class AvailabilityViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["id", "code", "name", "title", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]
