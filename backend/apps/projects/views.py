from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet
from apps.org.models import Organization
from apps.people.models import Person
from apps.rbac.models import Role
from .models import Activity, Project, Task
from .serializers import ActivitySerializer, ProjectSerializer, TaskSerializer
from .permissions import ActivityPermission, ProjectPermission, TaskPermission

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cache_key = f"dashboard_stats_user_{request.user.id}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        organizations = Organization.objects.count()
        people = Person.objects.count()
        projects = Project.objects.count()
        roles = Role.objects.count()

        payload = {
            "organizations": organizations,
            "people": people,
            "projects": projects,
            "roles": roles,
            "charts": [
                {"name": "Org", "total": organizations},
                {"name": "People", "total": people},
                {"name": "Projects", "total": projects},
                {"name": "Roles", "total": roles},
            ],
        }
        cache.set(cache_key, payload, timeout=60 * 5)
        return Response(payload)

class ProjectViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Project.objects.select_related("organization").all()
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission]
    search_fields = ["name", "code", "status"]
    ordering_fields = ["id", "name", "created_at"]


class ActivityViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Activity.objects.select_related("organization", "project", "contact_person").all()
    serializer_class = ActivitySerializer
    permission_classes = [ActivityPermission]
    search_fields = ["name", "description", "status", "project__name"]
    ordering_fields = ["id", "name", "status", "start_date", "created_at"]


class TaskViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Task.objects.select_related("organization", "project", "activity", "assigned_to").all()
    serializer_class = TaskSerializer
    permission_classes = [TaskPermission]
    search_fields = ["title", "description", "status", "priority", "project__name", "activity__name"]
    ordering_fields = ["id", "title", "status", "priority", "due_date", "created_at"]
