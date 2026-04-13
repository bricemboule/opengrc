from django.db.models import Count
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet

from .models import (
    ActionPlanTask,
    AuditFramework,
    CapacityAssessment,
    ContingencyPlan,
    CriticalInfrastructure,
    CyberStandard,
    DeliverableMilestone,
    DeskStudyReview,
    EmergencyResponseAsset,
    GovernanceArtifact,
    Phase,
    RiskRegisterEntry,
    SimulationExercise,
    Stakeholder,
    StakeholderConsultation,
    TrainingProgram,
)
from .serializers import (
    ActionPlanTaskSerializer,
    AuditFrameworkSerializer,
    CapacityAssessmentSerializer,
    ContingencyPlanSerializer,
    CriticalInfrastructureSerializer,
    CyberStandardSerializer,
    DeliverableMilestoneSerializer,
    DeskStudyReviewSerializer,
    EmergencyResponseAssetSerializer,
    GovernanceArtifactSerializer,
    RiskRegisterEntrySerializer,
    SimulationExerciseSerializer,
    StakeholderConsultationSerializer,
    StakeholderSerializer,
    TrainingProgramSerializer,
)


def scope_queryset_for_user(queryset, user):
    if user.is_superuser:
        return queryset
    if not getattr(user, "organization_id", None):
        return queryset.none()
    return queryset.filter(organization_id=user.organization_id)


PHASE_LABELS = dict(Phase.choices)


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


def sort_attention(items):
    return sorted(
        items,
        key=lambda item: (item["due_date"] is None, item["due_date"], item["title"]),
    )


class CyberGrcOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        stakeholders = scope_queryset_for_user(Stakeholder.objects.all(), request.user)
        infrastructure = scope_queryset_for_user(CriticalInfrastructure.objects.all(), request.user)
        artifacts = scope_queryset_for_user(GovernanceArtifact.objects.all(), request.user)
        desk_studies = scope_queryset_for_user(DeskStudyReview.objects.all(), request.user)
        consultations = scope_queryset_for_user(StakeholderConsultation.objects.all(), request.user)
        risks = scope_queryset_for_user(RiskRegisterEntry.objects.all(), request.user)
        capacity_assessments = scope_queryset_for_user(CapacityAssessment.objects.all(), request.user)
        plans = scope_queryset_for_user(ContingencyPlan.objects.all(), request.user)
        exercises = scope_queryset_for_user(SimulationExercise.objects.all(), request.user)
        standards = scope_queryset_for_user(CyberStandard.objects.all(), request.user)
        audits = scope_queryset_for_user(AuditFramework.objects.all(), request.user)
        trainings = scope_queryset_for_user(TrainingProgram.objects.all(), request.user)
        deliverables = scope_queryset_for_user(DeliverableMilestone.objects.all(), request.user)
        action_tasks = scope_queryset_for_user(ActionPlanTask.objects.all(), request.user)

        deliverables_by_phase = list(deliverables.values("phase").annotate(total=Count("id")).order_by("phase"))
        critical_risk_rows = risks.filter(risk_level__in=["high", "critical"]).select_related("infrastructure").order_by("-risk_score", "response_deadline")[:5]
        upcoming_exercise_rows = exercises.filter(status__in=["planned", "in_progress"]).order_by("planned_date", "id")[:5]
        due_deliverable_rows = deliverables.exclude(status__in=["completed", "validated", "archived"]).order_by("due_date", "planned_week", "id")[:5]
        desk_study_rows = desk_studies.exclude(status__in=["completed", "archived"]).order_by("due_date", "priority", "id")[:5]
        consultation_rows = consultations.exclude(status__in=["completed", "archived"]).order_by("planned_date", "next_follow_up_date", "id")[:5]
        capacity_rows = capacity_assessments.exclude(status__in=["completed", "archived"]).order_by("due_date", "gap_level", "id")[:5]
        action_plan_rows = action_tasks.exclude(status__in=["completed", "archived"]).order_by("due_date", "priority", "id")[:5]
        review_queue = (
            list(artifacts.exclude(next_review_date__isnull=True).order_by("next_review_date", "id")[:3])
            + list(standards.exclude(next_review_date__isnull=True).order_by("next_review_date", "id")[:3])
            + list(audits.exclude(next_review_date__isnull=True).order_by("next_review_date", "id")[:3])
            + list(plans.exclude(next_review_date__isnull=True).order_by("next_review_date", "id")[:3])
        )
        review_queue = sorted(
            review_queue,
            key=lambda item: (
                getattr(item, "next_review_date", None) is None,
                getattr(item, "next_review_date", None),
                item.id,
            ),
        )[:8]

        mapped_total = infrastructure.filter(mapping_status__in=["mapped", "reviewed"]).count()
        infrastructure_total = infrastructure.count()
        blocked_actions = action_tasks.exclude(status__in=["completed", "archived"]).exclude(blocker_summary="").count()
        open_desk_studies = desk_studies.exclude(status__in=["completed", "archived"]).count()
        pending_consultations = consultations.exclude(status__in=["completed", "archived"]).count()
        capacity_due = capacity_assessments.exclude(status__in=["completed", "archived"]).filter(due_date__lte=today).count()

        workflow_summary = [
            {
                "name": "Stakeholder engagement",
                "route": "cyber-stakeholders",
                "field": "status",
                "total": stakeholders.count(),
                "statuses": build_choice_summary(stakeholders, "status", Stakeholder._meta.get_field("status").choices),
            },
            {
                "name": "Desk study and document analysis",
                "route": "desk-study-reviews",
                "field": "status",
                "total": desk_studies.count(),
                "statuses": build_choice_summary(desk_studies, "status", DeskStudyReview._meta.get_field("status").choices),
            },
            {
                "name": "Consultation coordination",
                "route": "stakeholder-consultations",
                "field": "status",
                "total": consultations.count(),
                "statuses": build_choice_summary(consultations, "status", StakeholderConsultation._meta.get_field("status").choices),
            },
            {
                "name": "Infrastructure mapping",
                "route": "critical-infrastructure",
                "field": "mapping_status",
                "total": infrastructure_total,
                "statuses": build_choice_summary(infrastructure, "mapping_status", CriticalInfrastructure._meta.get_field("mapping_status").choices),
            },
            {
                "name": "Governance validation",
                "route": "governance-artifacts",
                "field": "status",
                "total": artifacts.count(),
                "statuses": build_choice_summary(artifacts, "status", GovernanceArtifact._meta.get_field("status").choices),
            },
            {
                "name": "Risk treatment",
                "route": "risk-register",
                "field": "treatment_status",
                "total": risks.count(),
                "statuses": build_choice_summary(risks, "treatment_status", RiskRegisterEntry._meta.get_field("treatment_status").choices),
            },
            {
                "name": "Capacity assessment",
                "route": "capacity-assessments",
                "field": "status",
                "total": capacity_assessments.count(),
                "statuses": build_choice_summary(capacity_assessments, "status", CapacityAssessment._meta.get_field("status").choices),
            },
            {
                "name": "Contingency readiness",
                "route": "contingency-plans",
                "field": "status",
                "total": plans.count(),
                "statuses": build_choice_summary(plans, "status", ContingencyPlan._meta.get_field("status").choices),
            },
            {
                "name": "Exercise cycle",
                "route": "simulation-exercises",
                "field": "status",
                "total": exercises.count(),
                "statuses": build_choice_summary(exercises, "status", SimulationExercise._meta.get_field("status").choices),
            },
            {
                "name": "Standards adoption",
                "route": "cyber-standards",
                "field": "status",
                "total": standards.count(),
                "statuses": build_choice_summary(standards, "status", CyberStandard._meta.get_field("status").choices),
            },
            {
                "name": "Audit rollout",
                "route": "audit-frameworks",
                "field": "status",
                "total": audits.count(),
                "statuses": build_choice_summary(audits, "status", AuditFramework._meta.get_field("status").choices),
            },
            {
                "name": "Training pipeline",
                "route": "training-programs",
                "field": "status",
                "total": trainings.count(),
                "statuses": build_choice_summary(trainings, "status", TrainingProgram._meta.get_field("status").choices),
            },
            {
                "name": "Deliverable tracking",
                "route": "deliverable-milestones",
                "field": "status",
                "total": deliverables.count(),
                "statuses": build_choice_summary(deliverables, "status", DeliverableMilestone._meta.get_field("status").choices),
            },
            {
                "name": "Action plan monitoring",
                "route": "action-plan-tasks",
                "field": "status",
                "total": action_tasks.count(),
                "statuses": build_choice_summary(action_tasks, "status", ActionPlanTask._meta.get_field("status").choices),
            },
        ]

        map_points = [
            {
                "id": item.id,
                "name": item.name,
                "code": item.code,
                "sector": item.sector,
                "location": item.location,
                "essential_service": item.essential_service,
                "latitude": item.latitude,
                "longitude": item.longitude,
                "mapping_status": item.get_mapping_status_display(),
                "criticality_level": item.get_criticality_level_display(),
            }
            for item in infrastructure.exclude(latitude__isnull=True).exclude(longitude__isnull=True).order_by("name", "id")
        ]

        attention_items = sort_attention(
            [
                *[
                    {
                        "type": "high_risk",
                        "title": risk.title,
                        "route": "risk-register",
                        "severity": risk.get_risk_level_display(),
                        "due_date": risk.response_deadline,
                        "context": risk.infrastructure.name if risk.infrastructure else "",
                    }
                    for risk in critical_risk_rows
                ],
                *[
                    {
                        "type": "deliverable",
                        "title": milestone.title,
                        "route": "deliverable-milestones",
                        "severity": milestone.get_status_display(),
                        "due_date": milestone.due_date,
                        "context": milestone.get_phase_display(),
                    }
                    for milestone in due_deliverable_rows
                ],
                *[
                    {
                        "type": "review",
                        "title": getattr(item, "title", str(item)),
                        "route": {
                            "GovernanceArtifact": "governance-artifacts",
                            "CyberStandard": "cyber-standards",
                            "AuditFramework": "audit-frameworks",
                            "ContingencyPlan": "contingency-plans",
                        }.get(item.__class__.__name__, ""),
                        "severity": item.get_status_display(),
                        "due_date": getattr(item, "next_review_date", None),
                        "context": item.__class__.__name__,
                    }
                    for item in review_queue
                ],
                *[
                    {
                        "type": "desk_study",
                        "title": item.title,
                        "route": "desk-study-reviews",
                        "severity": item.get_priority_display(),
                        "due_date": item.due_date,
                        "context": item.get_source_type_display(),
                    }
                    for item in desk_study_rows
                ],
                *[
                    {
                        "type": "consultation",
                        "title": item.title,
                        "route": "stakeholder-consultations",
                        "severity": item.get_status_display(),
                        "due_date": item.next_follow_up_date or item.planned_date,
                        "context": item.get_consultation_type_display(),
                    }
                    for item in consultation_rows
                ],
                *[
                    {
                        "type": "capacity",
                        "title": item.title,
                        "route": "capacity-assessments",
                        "severity": item.get_gap_level_display(),
                        "due_date": item.due_date,
                        "context": item.assessment_area,
                    }
                    for item in capacity_rows
                ],
                *[
                    {
                        "type": "action_plan",
                        "title": item.title,
                        "route": "action-plan-tasks",
                        "severity": "Blocked" if item.blocker_summary else item.get_status_display(),
                        "due_date": item.due_date,
                        "context": item.workstream,
                    }
                    for item in action_plan_rows if item.blocker_summary or item.due_date
                ],
            ],
        )[:12]

        payload = {
            "infrastructure_total": infrastructure_total,
            "mapped_infrastructure": mapped_total,
            "high_risks": risks.filter(risk_level__in=["high", "critical"]).count(),
            "contingency_plans": plans.count(),
            "standards": standards.count(),
            "audit_frameworks": audits.count(),
            "training_programs": trainings.count(),
            "simulation_exercises": exercises.count(),
            "messages_ready": True,
            "mapping_coverage": round((mapped_total / infrastructure_total) * 100, 1) if infrastructure_total else 0,
            "overdue_deliverables": deliverables.exclude(status__in=["completed", "validated", "archived"]).filter(due_date__lt=today).count(),
            "reviews_due": sum(1 for item in review_queue if getattr(item, "next_review_date", None) and item.next_review_date <= today),
            "blocked_actions": blocked_actions,
            "capacity_due": capacity_due,
            "pending_consultations": pending_consultations,
            "open_desk_studies": open_desk_studies,
            "priority_distribution": build_choice_summary(risks, "risk_level", RiskRegisterEntry._meta.get_field("risk_level").choices),
            "charts": [
                {"name": "Infrastructure", "total": infrastructure_total},
                {"name": "Desk Studies", "total": desk_studies.count()},
                {"name": "High Risks", "total": risks.filter(risk_level__in=["high", "critical"]).count()},
                {"name": "Capacity", "total": capacity_assessments.count()},
                {"name": "Consultations", "total": consultations.count()},
                {"name": "Plans", "total": plans.count()},
                {"name": "Actions", "total": action_tasks.count()},
                {"name": "Training", "total": trainings.count()},
            ],
            "deliverables_by_phase": [
                {
                    "name": PHASE_LABELS.get(item["phase"], item["phase"]),
                    "phase": item["phase"],
                    "total": item["total"],
                }
                for item in deliverables_by_phase
            ],
            "critical_risks": [
                {
                    "id": risk.id,
                    "title": risk.title,
                    "risk_level": risk.get_risk_level_display(),
                    "risk_score": risk.risk_score,
                    "response_deadline": risk.response_deadline,
                    "infrastructure_name": risk.infrastructure.name if risk.infrastructure else "",
                }
                for risk in critical_risk_rows
            ],
            "upcoming_exercises": [
                {
                    "id": exercise.id,
                    "title": exercise.title,
                    "exercise_type": exercise.get_exercise_type_display(),
                    "planned_date": exercise.planned_date,
                    "status": exercise.get_status_display(),
                }
                for exercise in upcoming_exercise_rows
            ],
            "due_deliverables": [
                {
                    "id": milestone.id,
                    "title": milestone.title,
                    "phase": milestone.get_phase_display(),
                    "due_date": milestone.due_date,
                    "status": milestone.get_status_display(),
                }
                for milestone in due_deliverable_rows
            ],
            "review_queue": [
                {
                    "id": item.id,
                    "title": getattr(item, "title", str(item)),
                    "type": item.__class__.__name__,
                    "next_review_date": getattr(item, "next_review_date", None),
                    "status": item.get_status_display(),
                }
                for item in review_queue
            ],
            "desk_study_queue": [
                {
                    "id": item.id,
                    "title": item.title,
                    "source_type": item.get_source_type_display(),
                    "priority": item.get_priority_display(),
                    "due_date": item.due_date,
                    "status": item.get_status_display(),
                }
                for item in desk_study_rows
            ],
            "consultation_queue": [
                {
                    "id": item.id,
                    "title": item.title,
                    "consultation_type": item.get_consultation_type_display(),
                    "planned_date": item.planned_date,
                    "next_follow_up_date": item.next_follow_up_date,
                    "status": item.get_status_display(),
                }
                for item in consultation_rows
            ],
            "capacity_queue": [
                {
                    "id": item.id,
                    "title": item.title,
                    "assessment_area": item.assessment_area,
                    "gap_level": item.get_gap_level_display(),
                    "due_date": item.due_date,
                    "status": item.get_status_display(),
                }
                for item in capacity_rows
            ],
            "action_plan_queue": [
                {
                    "id": item.id,
                    "title": item.title,
                    "workstream": item.workstream,
                    "priority": item.get_priority_display(),
                    "due_date": item.due_date,
                    "status": item.get_status_display(),
                    "blocked": bool(item.blocker_summary),
                }
                for item in action_plan_rows
            ],
            "workflow_summary": workflow_summary,
            "attention_items": attention_items,
            "map_points": map_points,
        }
        return Response(payload)


class StakeholderViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Stakeholder.objects.select_related("organization").all()
    serializer_class = StakeholderSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["name", "stakeholder_type", "sector", "focal_point", "email", "engagement_role"]
    ordering_fields = ["id", "name", "sector", "created_at"]


class CriticalInfrastructureViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = CriticalInfrastructure.objects.select_related("organization", "owner_stakeholder").all()
    serializer_class = CriticalInfrastructureSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["code", "name", "sector", "owner_name", "essential_service", "location"]
    ordering_fields = ["id", "name", "criticality_level", "mapping_status", "created_at"]


class GovernanceArtifactViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = GovernanceArtifact.objects.select_related("organization", "owner_stakeholder", "related_infrastructure").all()
    serializer_class = GovernanceArtifactSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "phase", "artifact_type", "version", "summary"]
    ordering_fields = ["id", "title", "phase", "status", "next_review_date", "created_at"]


class DeskStudyReviewViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = DeskStudyReview.objects.select_related("organization", "related_stakeholder", "related_infrastructure").all()
    serializer_class = DeskStudyReviewSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "source_type", "document_owner", "scope", "summary", "next_action"]
    ordering_fields = ["id", "title", "priority", "status", "due_date", "completed_date", "created_at"]


class StakeholderConsultationViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = StakeholderConsultation.objects.select_related("organization", "stakeholder", "related_infrastructure").all()
    serializer_class = StakeholderConsultationSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "consultation_type", "objective", "focal_person", "outcome_summary", "follow_up_actions"]
    ordering_fields = ["id", "title", "planned_date", "completed_date", "status", "next_follow_up_date", "created_at"]


class RiskRegisterEntryViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = RiskRegisterEntry.objects.select_related("organization", "infrastructure").all()
    serializer_class = RiskRegisterEntrySerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "category", "scenario", "risk_owner", "response_plan"]
    ordering_fields = ["id", "title", "risk_level", "risk_score", "response_deadline", "created_at"]


class CapacityAssessmentViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = CapacityAssessment.objects.select_related("organization", "infrastructure", "stakeholder").all()
    serializer_class = CapacityAssessmentSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "scope", "assessment_area", "lead_assessor", "baseline_summary", "priority_actions"]
    ordering_fields = ["id", "title", "gap_level", "status", "due_date", "completed_date", "created_at"]


class ContingencyPlanViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = ContingencyPlan.objects.select_related("organization").all()
    serializer_class = ContingencyPlanSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "plan_type", "scope", "communication_procedure", "coordination_mechanism"]
    ordering_fields = ["id", "title", "plan_type", "status", "next_review_date", "created_at"]


class EmergencyResponseAssetViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = EmergencyResponseAsset.objects.select_related("organization", "contingency_plan", "infrastructure").all()
    serializer_class = EmergencyResponseAssetSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["name", "asset_type", "owner_name", "location", "activation_notes"]
    ordering_fields = ["id", "name", "priority", "availability_status", "created_at"]


class SimulationExerciseViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = SimulationExercise.objects.select_related("organization", "contingency_plan").all()
    serializer_class = SimulationExerciseSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "exercise_type", "scenario", "participating_sectors", "findings", "lessons_learned"]
    ordering_fields = ["id", "title", "planned_date", "completed_date", "status", "created_at"]


class CyberStandardViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = CyberStandard.objects.select_related("organization").all()
    serializer_class = CyberStandardSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "standard_type", "target_sector", "owner_name", "summary"]
    ordering_fields = ["id", "title", "standard_type", "status", "next_review_date", "created_at"]


class AuditFrameworkViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = AuditFramework.objects.select_related("organization", "related_standard").all()
    serializer_class = AuditFrameworkSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "scope", "audit_frequency", "compliance_focus", "review_notes"]
    ordering_fields = ["id", "title", "status", "next_review_date", "created_at"]


class TrainingProgramViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = TrainingProgram.objects.select_related("organization").all()
    serializer_class = TrainingProgramSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "program_type", "target_audience", "delivery_mode", "summary"]
    ordering_fields = ["id", "title", "duration_days", "status", "created_at"]


class DeliverableMilestoneViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = DeliverableMilestone.objects.select_related("organization").all()
    serializer_class = DeliverableMilestoneSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "phase", "deliverable_category", "owner_name", "notes"]
    ordering_fields = ["id", "title", "phase", "status", "planned_week", "due_date", "created_at"]


class ActionPlanTaskViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = ActionPlanTask.objects.select_related("organization", "related_risk", "related_milestone", "related_infrastructure").all()
    serializer_class = ActionPlanTaskSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "workstream", "owner_name", "success_metric", "blocker_summary", "next_step"]
    ordering_fields = ["id", "title", "priority", "status", "start_date", "due_date", "completed_date", "created_at"]