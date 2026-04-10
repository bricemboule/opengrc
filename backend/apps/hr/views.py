from rest_framework import permissions
from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet
from .models import (
    Certificate,
    Department,
    JobTitle,
    Staff,
    StaffSkill,
    Team,
    TeamMember,
    TrainingCourse,
    TrainingEvent,
    TrainingParticipant,
)
from .serializers import (
    CertificateSerializer,
    DepartmentSerializer,
    JobTitleSerializer,
    StaffSerializer,
    StaffSkillSerializer,
    TeamMemberSerializer,
    TeamSerializer,
    TrainingCourseSerializer,
    TrainingEventSerializer,
    TrainingParticipantSerializer,
)


class DepartmentViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Department.objects.select_related("organization").all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["code", "name", "status"]
    ordering_fields = ["id", "name", "code", "created_at"]


class JobTitleViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = JobTitle.objects.select_related("organization").all()
    serializer_class = JobTitleSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["code", "name", "status"]
    ordering_fields = ["id", "name", "code", "created_at"]


class StaffViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Staff.objects.select_related("organization", "person", "department", "job_title").all()
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["code", "name", "status", "person__first_name", "person__last_name", "department__name", "job_title__name"]
    ordering_fields = ["id", "name", "code", "contract_end_date", "created_at"]


class TeamViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Team.objects.select_related("organization").all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["code", "name", "status"]
    ordering_fields = ["id", "name", "code", "created_at"]


class TeamMemberViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = TeamMember.objects.select_related("organization", "team", "staff").all()
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["team__name", "staff__name", "role", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]


class StaffSkillViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = StaffSkill.objects.select_related("organization", "staff", "skill").all()
    serializer_class = StaffSkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["staff__name", "skill__name", "proficiency", "status"]
    ordering_fields = ["id", "created_at", "updated_at"]


class TrainingCourseViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = TrainingCourse.objects.select_related("organization").all()
    serializer_class = TrainingCourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["code", "name", "status"]
    ordering_fields = ["id", "name", "code", "created_at"]


class CertificateViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Certificate.objects.select_related("organization").all()
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["code", "name", "status"]
    ordering_fields = ["id", "name", "code", "created_at"]


class TrainingEventViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = TrainingEvent.objects.select_related("organization", "training_course", "certificate").all()
    serializer_class = TrainingEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["code", "name", "status", "training_course__name", "certificate__name"]
    ordering_fields = ["id", "name", "start_date", "end_date", "created_at"]


class TrainingParticipantViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = TrainingParticipant.objects.select_related("organization", "training_event", "staff").all()
    serializer_class = TrainingParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["training_event__name", "staff__name", "completion_status"]
    ordering_fields = ["id", "created_at", "updated_at"]
