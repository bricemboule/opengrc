from django.db.models import Count, Q
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet

from .models import (
    AssetAllocation,
    Incident,
    IncidentAssignment,
    IncidentAttachment,
    IncidentCommunication,
    IncidentTask,
    IncidentUpdate,
    SOPExecution,
    SOPExecutionStep,
    SOPStep,
    SOPTemplate,
)
from .serializers import (
    AssetAllocationSerializer,
    IncidentAssignmentSerializer,
    IncidentAttachmentSerializer,
    IncidentCommunicationSerializer,
    IncidentSerializer,
    IncidentTaskSerializer,
    IncidentUpdateSerializer,
    SOPExecutionSerializer,
    SOPExecutionStepSerializer,
    SOPStepSerializer,
    SOPTemplateSerializer,
)


def scope_queryset_for_user(queryset, user):
    if user.is_superuser:
        return queryset
    if not getattr(user, "organization_id", None):
        return queryset.none()
    return queryset.filter(organization_id=user.organization_id)


def build_choice_summary(queryset, field_name, choices):
    counts = {
        item[field_name]: item["total"]
        for item in queryset.values(field_name).annotate(total=Count("id"))
    }
    return [
        {
            "value": value,
            "label": label,
            "total": counts.get(value, 0),
        }
        for value, label in choices
    ]


class IncidentViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Incident.objects.select_related("organization", "incident_coordinator", "lead_stakeholder", "linked_plan").prefetch_related(
        "affected_sectors",
        "affected_infrastructure",
    )
    serializer_class = IncidentSerializer
    filterset_fields = ["incident_type", "severity", "status", "source", "national_significance"]
    search_fields = ["title", "summary", "external_reference", "cross_sector_impact"]
    ordering_fields = ["reported_at", "detected_at", "next_update_due", "severity", "status", "created_at"]
    ordering = ["-reported_at", "-created_at", "-id"]

    @action(detail=True, methods=["get"], url_path="timeline")
    def timeline(self, request, pk=None):
        incident = self.get_object()
        payload = {
            "incident": self.get_serializer(incident).data,
            "updates": IncidentUpdateSerializer(incident.updates.all()[:10], many=True).data,
            "tasks": IncidentTaskSerializer(incident.tasks.all()[:10], many=True).data,
            "assignments": IncidentAssignmentSerializer(incident.assignments.all()[:10], many=True).data,
            "communications": IncidentCommunicationSerializer(incident.communications.all()[:10], many=True).data,
            "attachments": IncidentAttachmentSerializer(incident.attachments.all()[:10], many=True).data,
        }
        return Response(payload)

    @action(detail=False, methods=["get"], url_path="command-overview")
    def command_overview(self, request):
        incidents = scope_queryset_for_user(self.get_queryset(), request.user)
        today = timezone.now()
        active_incidents = incidents.exclude(status="closed")
        severe_incidents = incidents.filter(severity__in=["high", "critical", "national"]).order_by("-reported_at", "-id")[:5]
        update_due = active_incidents.filter(next_update_due__isnull=False, next_update_due__lte=today).order_by("next_update_due", "id")[:6]

        return Response(
            {
                "total": incidents.count(),
                "active": active_incidents.count(),
                "high_severity": incidents.filter(severity__in=["high", "critical", "national"]).count(),
                "status_summary": build_choice_summary(incidents, "status", Incident._meta.get_field("status").choices),
                "severe_incidents": IncidentSerializer(severe_incidents, many=True).data,
                "update_due": IncidentSerializer(update_due, many=True).data,
            }
        )


class IncidentUpdateViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = IncidentUpdate.objects.select_related("organization", "incident")
    serializer_class = IncidentUpdateSerializer
    filterset_fields = ["incident", "update_type", "status_snapshot", "severity_snapshot"]
    search_fields = ["title", "message", "next_step"]
    ordering_fields = ["recorded_at", "created_at"]
    ordering = ["-recorded_at", "-id"]


class IncidentTaskViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = IncidentTask.objects.select_related("organization", "incident", "assigned_to")
    serializer_class = IncidentTaskSerializer
    filterset_fields = ["incident", "status", "priority", "assigned_to"]
    search_fields = ["title", "description", "blocker_summary", "next_step"]
    ordering_fields = ["due_at", "completed_at", "created_at", "status", "priority"]
    ordering = ["due_at", "-created_at", "-id"]


class IncidentAssignmentViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = IncidentAssignment.objects.select_related("organization", "incident", "assignee", "stakeholder")
    serializer_class = IncidentAssignmentSerializer
    filterset_fields = ["incident", "status", "assignee", "stakeholder"]
    search_fields = ["role_in_response", "notes"]
    ordering_fields = ["assigned_at", "acknowledged_at", "released_at", "created_at"]
    ordering = ["-assigned_at", "-id"]


class IncidentCommunicationViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = IncidentCommunication.objects.select_related("organization", "incident")
    serializer_class = IncidentCommunicationSerializer
    filterset_fields = ["incident", "direction", "channel", "requires_acknowledgement"]
    search_fields = ["subject", "audience", "message", "external_reference"]
    ordering_fields = ["sent_at", "created_at"]
    ordering = ["-sent_at", "-id"]


class IncidentAttachmentViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = IncidentAttachment.objects.select_related("organization", "incident")
    serializer_class = IncidentAttachmentSerializer
    filterset_fields = ["incident", "attachment_type"]
    search_fields = ["title", "reference_label", "notes"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at", "-id"]


class SOPTemplateViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = SOPTemplate.objects.select_related(
        "organization",
        "contingency_plan",
        "related_artifact",
        "related_infrastructure",
        "owner_stakeholder",
    )
    serializer_class = SOPTemplateSerializer
    filterset_fields = ["status", "contingency_plan", "related_artifact", "related_infrastructure", "owner_stakeholder"]
    search_fields = ["code", "title", "objective", "activation_trigger", "notes"]
    ordering_fields = ["title", "code", "status", "last_reviewed_at", "created_at"]
    ordering = ["title", "-id"]


class SOPStepViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = SOPStep.objects.select_related("organization", "template", "default_assignee")
    serializer_class = SOPStepSerializer
    filterset_fields = ["template", "step_type", "is_required", "default_assignee"]
    search_fields = ["title", "instruction", "responsible_role", "evidence_hint", "escalation_hint"]
    ordering_fields = ["template", "step_order", "step_type", "created_at"]
    ordering = ["template", "step_order", "id"]


class SOPExecutionViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = SOPExecution.objects.select_related("organization", "incident", "template", "execution_commander")
    serializer_class = SOPExecutionSerializer
    filterset_fields = ["incident", "template", "status", "execution_commander"]
    search_fields = ["title", "summary", "outcome_summary", "blocker_summary", "next_action"]
    ordering_fields = ["started_at", "target_completion_at", "completed_at", "created_at", "status"]
    ordering = ["-started_at", "-created_at", "-id"]

    @action(detail=True, methods=["get"], url_path="step-board")
    def step_board(self, request, pk=None):
        execution = self.get_object()
        steps = execution.steps.select_related("assigned_to", "completed_by", "template_step").all()
        payload = {
            "execution": self.get_serializer(execution).data,
            "step_summary": build_choice_summary(steps, "status", SOPExecutionStep._meta.get_field("status").choices),
            "steps": SOPExecutionStepSerializer(steps, many=True).data,
        }
        return Response(payload)


class SOPExecutionStepViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = SOPExecutionStep.objects.select_related("organization", "execution", "template_step", "assigned_to", "completed_by")
    serializer_class = SOPExecutionStepSerializer
    filterset_fields = ["execution", "status", "assigned_to", "completed_by", "step_type"]
    search_fields = ["title", "instruction", "blocker_summary", "notes"]
    ordering_fields = ["execution", "step_order", "status", "started_at", "completed_at", "created_at"]
    ordering = ["execution", "step_order", "id"]


class AssetAllocationViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = AssetAllocation.objects.select_related(
        "organization",
        "incident",
        "emergency_asset",
        "destination_infrastructure",
        "related_task",
        "approved_by",
        "requested_by",
        "emergency_asset__infrastructure",
    )
    serializer_class = AssetAllocationSerializer
    filterset_fields = ["incident", "emergency_asset", "destination_infrastructure", "related_task", "status", "priority"]
    search_fields = ["title", "destination", "deployment_notes", "release_notes", "incident__title", "emergency_asset__name"]
    ordering_fields = ["requested_at", "approved_at", "mobilized_at", "deployed_at", "released_at", "priority", "status", "created_at"]
    ordering = ["-requested_at", "-id"]

    @action(detail=False, methods=["get"], url_path="allocation-overview")
    def allocation_overview(self, request):
        allocations = scope_queryset_for_user(self.get_queryset(), request.user)
        payload = {
            "total": allocations.count(),
            "status_summary": build_choice_summary(allocations, "status", AssetAllocation._meta.get_field("status").choices),
            "priority_summary": build_choice_summary(allocations, "priority", AssetAllocation._meta.get_field("priority").choices),
            "due_for_release": AssetAllocationSerializer(
                allocations.filter(status__in=["deployed", "demobilizing"]).order_by("deployed_at", "requested_at", "id")[:6],
                many=True,
            ).data,
        }
        return Response(payload)


class IncidentOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        incidents = scope_queryset_for_user(Incident.objects.all(), request.user)
        tasks = scope_queryset_for_user(IncidentTask.objects.all(), request.user)
        sop_executions = scope_queryset_for_user(SOPExecution.objects.all(), request.user)
        allocations = scope_queryset_for_user(AssetAllocation.objects.all(), request.user)
        now = timezone.now()

        severe = incidents.filter(severity__in=["high", "critical", "national"]).order_by("-reported_at", "-id")[:6]
        due_updates = incidents.exclude(status="closed").filter(next_update_due__isnull=False, next_update_due__lte=now).order_by("next_update_due", "id")[:6]
        blocked_tasks = tasks.filter(Q(status="blocked") | ~Q(blocker_summary="")).order_by("due_at", "id")[:6]

        return Response(
            {
                "total": incidents.count(),
                "active": incidents.exclude(status="closed").count(),
                "high_severity": incidents.filter(severity__in=["high", "critical", "national"]).count(),
                "status_summary": build_choice_summary(incidents, "status", Incident._meta.get_field("status").choices),
                "severe_incidents": IncidentSerializer(severe, many=True).data,
                "due_updates": IncidentSerializer(due_updates, many=True).data,
                "blocked_tasks": IncidentTaskSerializer(blocked_tasks, many=True).data,
                "active_sop_executions": sop_executions.filter(status__in=["planned", "active", "blocked"]).count(),
                "active_allocations": allocations.filter(status__in=["approved", "mobilizing", "deployed", "demobilizing"]).count(),
            }
        )
