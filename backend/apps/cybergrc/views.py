from collections import Counter
from datetime import timedelta

from django.core.files.base import ContentFile
from django.db.models import Count, DateTimeField, Q
from django.db.models.functions import Cast, Coalesce
from django.http import HttpResponse
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet

from .document_generation import TEXT_CONTENT_TYPES, build_document_payload, build_document_summary
from .models import (
    Acknowledgement,
    ActionPlanTask,
    AssetInventoryItem,
    AuditFramework,
    AuditChecklist,
    AuditFinding,
    AuditPlan,
    CapacityAssessment,
    ConformityAssessment,
    ContingencyPlan,
    ControlEvidence,
    CorrectiveAction,
    CriticalInfrastructure,
    CyberStandard,
    DeliverableMilestone,
    DeskStudyReview,
    DistributionGroup,
    EmergencyResponseAsset,
    GeneratedDocument,
    GovernanceArtifact,
    Indicator,
    InformationShare,
    ChangeLogEntry,
    NonConformity,
    RiskAssessmentReview,
    Phase,
    RiskRegisterEntry,
    RiskScenario,
    ReviewCycle,
    ReviewRecord,
    Sector,
    SimulationExercise,
    StandardControl,
    StandardRequirement,
    Stakeholder,
    StakeholderConsultation,
    ThreatBulletin,
    ThreatEvent,
    TrainingProgram,
    VulnerabilityRecord,
)
from .serializers import (
    AcknowledgementSerializer,
    ActionPlanTaskSerializer,
    AssetInventoryItemSerializer,
    AuditFrameworkSerializer,
    AuditChecklistSerializer,
    AuditFindingSerializer,
    AuditPlanSerializer,
    CapacityAssessmentSerializer,
    ConformityAssessmentSerializer,
    ContingencyPlanSerializer,
    ControlEvidenceSerializer,
    CorrectiveActionSerializer,
    CriticalInfrastructureSerializer,
    CyberStandardSerializer,
    DeliverableMilestoneSerializer,
    DeskStudyReviewSerializer,
    DistributionGroupSerializer,
    EmergencyResponseAssetSerializer,
    GeneratedDocumentSerializer,
    GenerateReportDocumentSerializer,
    GovernanceArtifactSerializer,
    IndicatorSerializer,
    InformationShareSerializer,
    ChangeLogEntrySerializer,
    NonConformitySerializer,
    RiskAssessmentReviewSerializer,
    RiskRegisterEntrySerializer,
    RiskScenarioSerializer,
    ReviewCycleSerializer,
    ReviewRecordSerializer,
    SectorSerializer,
    SimulationExerciseSerializer,
    StandardControlSerializer,
    StandardRequirementSerializer,
    StakeholderConsultationSerializer,
    StakeholderSerializer,
    ThreatBulletinSerializer,
    ThreatEventSerializer,
    TrainingProgramSerializer,
    VulnerabilityRecordSerializer,
)
from .spatial import apply_spatial_filters, build_feature_collection, spatial_backend_summary


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


def normalize_due_sort_value(value):
    if value is None:
        return ""
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def sort_attention(items):
    return sorted(
        items,
        key=lambda item: (item["due_date"] is None, normalize_due_sort_value(item["due_date"]), item["title"]),
    )


def annotate_consultation_schedule(queryset):
    return queryset.annotate(schedule_anchor=Coalesce("start_datetime", Cast("planned_date", output_field=DateTimeField())))


class CyberGrcOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        stakeholders = scope_queryset_for_user(Stakeholder.objects.all(), request.user)
        infrastructure = scope_queryset_for_user(CriticalInfrastructure.objects.all(), request.user)
        artifacts = scope_queryset_for_user(GovernanceArtifact.objects.all(), request.user)
        desk_studies = scope_queryset_for_user(DeskStudyReview.objects.all(), request.user)
        consultations = annotate_consultation_schedule(scope_queryset_for_user(StakeholderConsultation.objects.all(), request.user))
        risks = scope_queryset_for_user(RiskRegisterEntry.objects.all(), request.user)
        asset_inventory = scope_queryset_for_user(AssetInventoryItem.objects.all(), request.user)
        threat_events = scope_queryset_for_user(ThreatEvent.objects.all(), request.user)
        vulnerabilities = scope_queryset_for_user(VulnerabilityRecord.objects.all(), request.user)
        risk_scenarios = scope_queryset_for_user(RiskScenario.objects.all(), request.user)
        risk_reviews = scope_queryset_for_user(RiskAssessmentReview.objects.all(), request.user)
        threat_bulletins = scope_queryset_for_user(ThreatBulletin.objects.all(), request.user)
        information_shares = scope_queryset_for_user(InformationShare.objects.all(), request.user)
        generated_documents = scope_queryset_for_user(GeneratedDocument.objects.all(), request.user)
        review_cycles = scope_queryset_for_user(ReviewCycle.objects.all(), request.user)
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
        critical_threat_rows = threat_events.filter(severity__in=["high", "critical"]).select_related("related_infrastructure").order_by("status", "-first_seen_at", "id")[:5]
        due_risk_review_rows = risk_reviews.exclude(status__in=["completed", "archived"]).filter(
            Q(follow_up_date__isnull=False) | Q(review_date__isnull=False)
        ).order_by("follow_up_date", "review_date", "id")[:5]
        pending_share_rows = information_shares.exclude(status__in=["closed"]).filter(
            Q(acknowledgement_due_date__isnull=False) | Q(shared_at__isnull=False)
        ).order_by("acknowledgement_due_date", "shared_at", "id")[:5]
        review_cycle_rows = review_cycles.exclude(status__in=["completed", "archived"]).filter(next_review_date__isnull=False).order_by("next_review_date", "id")[:5]
        generated_document_rows = generated_documents.exclude(status__in=["approved", "archived", "superseded"]).order_by("-generated_on", "id")[:5]
        upcoming_exercise_rows = exercises.filter(status__in=["planned", "in_progress"]).order_by("planned_date", "id")[:5]
        due_deliverable_rows = deliverables.exclude(status__in=["completed", "validated", "archived"]).order_by("due_date", "planned_week", "id")[:5]
        desk_study_rows = desk_studies.exclude(status__in=["completed", "archived"]).order_by("due_date", "priority", "id")[:5]
        consultation_rows = consultations.exclude(status__in=["completed", "missed", "archived"]).filter(Q(start_datetime__isnull=False) | Q(planned_date__isnull=False) | Q(next_follow_up_date__isnull=False)).order_by("schedule_anchor", "next_follow_up_date", "id")[:5]
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
        pending_consultations = consultations.exclude(status__in=["completed", "missed", "archived"]).count()
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
                "name": "Asset inventory",
                "route": "asset-inventory",
                "field": "status",
                "total": asset_inventory.count(),
                "statuses": build_choice_summary(asset_inventory, "status", AssetInventoryItem._meta.get_field("status").choices),
            },
            {
                "name": "Risk treatment",
                "route": "risk-register",
                "field": "treatment_status",
                "total": risks.count(),
                "statuses": build_choice_summary(risks, "treatment_status", RiskRegisterEntry._meta.get_field("treatment_status").choices),
            },
            {
                "name": "Threat monitoring",
                "route": "threat-events",
                "field": "status",
                "total": threat_events.count(),
                "statuses": build_choice_summary(threat_events, "status", ThreatEvent._meta.get_field("status").choices),
            },
            {
                "name": "Vulnerability tracking",
                "route": "vulnerability-records",
                "field": "status",
                "total": vulnerabilities.count(),
                "statuses": build_choice_summary(vulnerabilities, "status", VulnerabilityRecord._meta.get_field("status").choices),
            },
            {
                "name": "Risk scenario design",
                "route": "risk-scenarios",
                "field": "status",
                "total": risk_scenarios.count(),
                "statuses": build_choice_summary(risk_scenarios, "status", RiskScenario._meta.get_field("status").choices),
            },
            {
                "name": "Threat information sharing",
                "route": "information-shares",
                "field": "status",
                "total": information_shares.count(),
                "statuses": build_choice_summary(information_shares, "status", InformationShare._meta.get_field("status").choices),
            },
            {
                "name": "Document generation",
                "route": "generated-documents",
                "field": "status",
                "total": generated_documents.count(),
                "statuses": build_choice_summary(generated_documents, "status", GeneratedDocument._meta.get_field("status").choices),
            },
            {
                "name": "Review cadence",
                "route": "review-cycles",
                "field": "status",
                "total": review_cycles.count(),
                "statuses": build_choice_summary(review_cycles, "status", ReviewCycle._meta.get_field("status").choices),
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
        ] + [
            {
                "id": f"asset-{item.id}",
                "name": item.name,
                "code": item.code,
                "sector": item.sector,
                "location": item.location or item.admin_area,
                "essential_service": item.essential_function,
                "latitude": item.latitude,
                "longitude": item.longitude,
                "mapping_status": item.get_status_display(),
                "criticality_level": item.get_criticality_level_display(),
            }
            for item in asset_inventory.exclude(latitude__isnull=True).exclude(longitude__isnull=True).order_by("name", "id")
        ] + [
            {
                "id": f"threat-{item.id}",
                "name": item.title,
                "code": item.get_threat_type_display(),
                "sector": item.related_infrastructure.sector if item.related_infrastructure else "",
                "location": item.location or item.admin_area,
                "essential_service": item.summary,
                "latitude": item.latitude,
                "longitude": item.longitude,
                "mapping_status": item.get_status_display(),
                "criticality_level": item.get_severity_display(),
            }
            for item in threat_events.exclude(latitude__isnull=True).exclude(longitude__isnull=True).select_related("related_infrastructure").order_by("title", "id")
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
                        "type": "threat_event",
                        "title": event.title,
                        "route": "threat-events",
                        "severity": event.get_severity_display(),
                        "due_date": event.last_seen_at or event.first_seen_at,
                        "context": " / ".join(part for part in [event.get_threat_type_display(), event.related_infrastructure.name if event.related_infrastructure else ""] if part),
                    }
                    for event in critical_threat_rows
                ],
                *[
                    {
                        "type": "risk_review",
                        "title": review.title,
                        "route": "risk-assessment-reviews",
                        "severity": review.get_residual_risk_level_display(),
                        "due_date": review.follow_up_date or review.review_date,
                        "context": review.get_decision_display(),
                    }
                    for review in due_risk_review_rows
                ],
                *[
                    {
                        "type": "information_share",
                        "title": share.title,
                        "route": "information-shares",
                        "severity": share.get_status_display(),
                        "due_date": share.acknowledgement_due_date or share.shared_at,
                        "context": share.get_share_channel_display(),
                    }
                    for share in pending_share_rows
                ],
                *[
                    {
                        "type": "review_cycle",
                        "title": cycle.title,
                        "route": "review-cycles",
                        "severity": cycle.get_status_display(),
                        "due_date": cycle.next_review_date,
                        "context": cycle.current_version_label or cycle.module_label,
                    }
                    for cycle in review_cycle_rows
                ],
                *[
                    {
                        "type": "generated_document",
                        "title": document.title,
                        "route": "generated-documents",
                        "severity": document.get_status_display(),
                        "due_date": document.generated_on,
                        "context": document.version_label or document.module_label,
                    }
                    for document in generated_document_rows
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
                        "due_date": item.start_datetime or item.next_follow_up_date or item.planned_date,
                        "context": " ? ".join(part for part in [item.get_consultation_type_display(), item.get_engagement_channel_display()] if part),
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
            "asset_inventory": asset_inventory.count(),
            "threat_events": threat_events.count(),
            "risk_scenarios": risk_scenarios.count(),
            "threat_bulletins": threat_bulletins.count(),
            "generated_documents": generated_documents.count(),
            "review_cycles": review_cycles.count(),
            "messages_ready": True,
            "mapping_coverage": round((mapped_total / infrastructure_total) * 100, 1) if infrastructure_total else 0,
            "overdue_deliverables": deliverables.exclude(status__in=["completed", "validated", "archived"]).filter(due_date__lt=today).count(),
            "reviews_due": sum(1 for item in review_queue if getattr(item, "next_review_date", None) and item.next_review_date <= today)
            + review_cycles.exclude(status__in=["completed", "archived"]).filter(next_review_date__lte=today).count(),
            "blocked_actions": blocked_actions,
            "capacity_due": capacity_due,
            "pending_consultations": pending_consultations,
            "open_desk_studies": open_desk_studies,
            "priority_distribution": build_choice_summary(risks, "risk_level", RiskRegisterEntry._meta.get_field("risk_level").choices),
            "charts": [
                {"name": "Infrastructure", "total": infrastructure_total},
                {"name": "Assets", "total": asset_inventory.count()},
                {"name": "Desk Studies", "total": desk_studies.count()},
                {"name": "High Risks", "total": risks.filter(risk_level__in=["high", "critical"]).count()},
                {"name": "Threats", "total": threat_events.count()},
                {"name": "Scenarios", "total": risk_scenarios.count()},
                {"name": "Capacity", "total": capacity_assessments.count()},
                {"name": "Consultations", "total": consultations.count()},
                {"name": "Plans", "total": plans.count()},
                {"name": "Bulletins", "total": threat_bulletins.count()},
                {"name": "Shares", "total": information_shares.count()},
                {"name": "Documents", "total": generated_documents.count()},
                {"name": "Review Cycles", "total": review_cycles.count()},
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
                    "engagement_channel": item.get_engagement_channel_display(),
                    "planned_date": item.planned_date,
                    "start_datetime": item.start_datetime,
                    "end_datetime": item.end_datetime,
                    "meeting_location": item.meeting_location,
                    "meeting_link": item.meeting_link,
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


class SectorViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Sector.objects.select_related("organization").all()
    serializer_class = SectorSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["code", "name", "description", "status"]
    ordering_fields = ["id", "name", "code", "status", "created_at"]


class StakeholderViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Stakeholder.objects.select_related("organization", "sector_ref").all()
    serializer_class = StakeholderSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["name", "stakeholder_type", "sector", "sector_ref__name", "focal_point", "email", "engagement_role"]
    ordering_fields = ["id", "name", "sector", "created_at"]


class SpatialDatasetViewSetMixin:
    spatial_lat_field = "latitude"
    spatial_lng_field = "longitude"
    spatial_title_field = "name"
    spatial_status_field = "status"
    spatial_sector_field = "sector"
    spatial_area_field = "admin_area"
    spatial_location_field = "location"

    def get_queryset(self):
        queryset = super().get_queryset()
        request = getattr(self, "request", None)
        if not request:
            return queryset
        if getattr(self, "action", None) in {"list", "geojson", "spatial_summary"}:
            queryset = apply_spatial_filters(
                queryset,
                request,
                lat_field=self.spatial_lat_field,
                lng_field=self.spatial_lng_field,
            )
        return queryset

    def _spatial_rows(self):
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "id",
            self.spatial_title_field,
            self.spatial_status_field,
            self.spatial_sector_field,
            self.spatial_area_field,
            self.spatial_location_field,
            self.spatial_lat_field,
            self.spatial_lng_field,
        ]
        rows = list(queryset.values(*fields))
        return rows

    @action(detail=False, methods=["get"], url_path="geojson")
    def geojson(self, request):
        return Response(
            build_feature_collection(
                self._spatial_rows(),
                title_field=self.spatial_title_field,
                lat_field=self.spatial_lat_field,
                lng_field=self.spatial_lng_field,
                status_field=self.spatial_status_field,
            )
        )

    @action(detail=False, methods=["get"], url_path="spatial-summary")
    def spatial_summary(self, request):
        rows = self._spatial_rows()
        geolocated = [row for row in rows if row.get(self.spatial_lat_field) is not None and row.get(self.spatial_lng_field) is not None]
        bounds = None
        if geolocated:
            latitudes = [float(row[self.spatial_lat_field]) for row in geolocated]
            longitudes = [float(row[self.spatial_lng_field]) for row in geolocated]
            bounds = {
                "min_lat": min(latitudes),
                "max_lat": max(latitudes),
                "min_lng": min(longitudes),
                "max_lng": max(longitudes),
            }

        top_sectors = Counter(row.get(self.spatial_sector_field) or "Unspecified sector" for row in geolocated).most_common(5)
        top_areas = Counter((row.get(self.spatial_area_field) or row.get(self.spatial_location_field) or "Unspecified area") for row in geolocated).most_common(5)

        return Response(
            {
                "engine": spatial_backend_summary(),
                "total_rows": len(rows),
                "geolocated_rows": len(geolocated),
                "bounds": bounds,
                "top_sectors": [{"label": label, "count": count} for label, count in top_sectors],
                "top_areas": [{"label": label, "count": count} for label, count in top_areas],
            }
        )


class CriticalInfrastructureViewSet(SpatialDatasetViewSetMixin, OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = CriticalInfrastructure.objects.select_related("organization", "owner_stakeholder", "sector_ref").all()
    serializer_class = CriticalInfrastructureSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["code", "name", "sector", "sector_ref__name", "owner_name", "essential_service", "location"]
    ordering_fields = ["id", "name", "criticality_level", "mapping_status", "created_at"]
    spatial_status_field = "mapping_status"


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
    search_fields = [
        "title",
        "consultation_type",
        "engagement_channel",
        "objective",
        "agenda",
        "attendees",
        "focal_person",
        "meeting_location",
        "meeting_link",
        "dial_in_details",
        "outcome_summary",
        "minutes",
        "follow_up_actions",
    ]
    ordering_fields = [
        "id",
        "title",
        "planned_date",
        "start_datetime",
        "end_datetime",
        "completed_date",
        "status",
        "next_follow_up_date",
        "created_at",
    ]

    @action(detail=False, methods=["get"], url_path="upcoming")
    def upcoming(self, request):
        horizon_days = max(1, min(int(request.query_params.get("days", 60)), 120))
        now = timezone.now()
        today = timezone.localdate()
        follow_up_horizon = today + timedelta(days=horizon_days)
        schedule_horizon = now + timedelta(days=horizon_days)

        queryset = annotate_consultation_schedule(self.filter_queryset(self.get_queryset()))
        queryset = queryset.exclude(status__in=["completed", "missed", "archived"]).filter(
            Q(start_datetime__isnull=False, start_datetime__gte=now, start_datetime__lte=schedule_horizon)
            | Q(start_datetime__isnull=True, planned_date__isnull=False, planned_date__gte=today, planned_date__lte=follow_up_horizon)
            | Q(next_follow_up_date__isnull=False, next_follow_up_date__gte=today, next_follow_up_date__lte=follow_up_horizon)
        ).order_by("schedule_anchor", "next_follow_up_date", "id")[:100]

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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


class EmergencyResponseAssetViewSet(SpatialDatasetViewSetMixin, OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = EmergencyResponseAsset.objects.select_related("organization", "contingency_plan", "infrastructure", "owner_stakeholder").all()
    serializer_class = EmergencyResponseAssetSerializer
    permission_classes = [IsAuthenticated]
    search_fields = [
        "name",
        "asset_type",
        "owner_name",
        "owner_stakeholder__name",
        "location",
        "activation_notes",
        "deployment_status",
    ]
    ordering_fields = [
        "id",
        "name",
        "priority",
        "availability_status",
        "deployment_status",
        "mobilization_eta_minutes",
        "capacity_units",
        "last_readiness_check",
        "created_at",
    ]
    spatial_sector_field = "owner_name"
    spatial_area_field = "location"
    spatial_status_field = "availability_status"


class SimulationExerciseViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = SimulationExercise.objects.select_related("organization", "contingency_plan").all()
    serializer_class = SimulationExerciseSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "exercise_type", "scenario", "participating_sectors", "findings", "lessons_learned"]
    ordering_fields = ["id", "title", "planned_date", "completed_date", "status", "created_at"]


class CyberStandardViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = CyberStandard.objects.select_related("organization", "target_sector_ref").all()
    serializer_class = CyberStandardSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "standard_type", "target_sector", "target_sector_ref__name", "owner_name", "summary"]
    ordering_fields = ["id", "title", "standard_type", "status", "next_review_date", "created_at"]


class AuditFrameworkViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = AuditFramework.objects.select_related("organization", "related_standard").all()
    serializer_class = AuditFrameworkSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "scope", "audit_frequency", "compliance_focus", "review_notes"]
    ordering_fields = ["id", "title", "status", "next_review_date", "created_at"]


class StandardRequirementViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = StandardRequirement.objects.select_related("organization", "related_standard").all()
    serializer_class = StandardRequirementSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["code", "title", "chapter", "owner_name", "summary", "implementation_guidance", "verification_method"]
    ordering_fields = ["id", "code", "title", "status", "priority", "sort_order", "created_at"]


class StandardControlViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = StandardControl.objects.select_related("organization", "related_standard", "related_requirement").all()
    serializer_class = StandardControlSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["code", "title", "domain", "owner_name", "control_objective", "control_procedure", "measurement_criteria"]
    ordering_fields = ["id", "code", "title", "status", "priority", "sort_order", "created_at"]


class ConformityAssessmentViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = ConformityAssessment.objects.select_related(
        "organization",
        "related_standard",
        "related_requirement",
        "related_control",
        "related_framework",
        "target_stakeholder",
        "related_infrastructure",
    ).all()
    serializer_class = ConformityAssessmentSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "assessor_name", "evidence_summary", "gap_summary", "recommendation_summary", "follow_up_action"]
    ordering_fields = ["id", "title", "status", "conformity_level", "assessed_on", "next_review_date", "score", "created_at"]


class ControlEvidenceViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = ControlEvidence.objects.select_related(
        "organization",
        "related_assessment",
        "related_standard",
        "related_requirement",
        "related_control",
    ).all()
    serializer_class = ControlEvidenceSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "reference_label", "owner_name", "reference_url", "notes"]
    ordering_fields = ["id", "title", "status", "captured_on", "validity_until", "created_at"]


class AuditPlanViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = AuditPlan.objects.select_related(
        "organization",
        "related_framework",
        "related_standard",
        "target_stakeholder",
        "related_infrastructure",
    ).all()
    serializer_class = AuditPlanSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "scope", "lead_auditor", "summary", "next_step"]
    ordering_fields = ["id", "title", "status", "planned_start_date", "planned_end_date", "actual_end_date", "created_at"]


class AuditChecklistViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = AuditChecklist.objects.select_related("organization", "audit_plan", "related_requirement", "related_control").all()
    serializer_class = AuditChecklistSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "verification_procedure", "expected_evidence", "finding_summary", "notes"]
    ordering_fields = ["id", "title", "status", "item_order", "created_at"]


class AuditFindingViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = AuditFinding.objects.select_related(
        "organization",
        "audit_plan",
        "checklist_item",
        "related_assessment",
        "related_requirement",
        "related_control",
    ).all()
    serializer_class = AuditFindingSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "owner_name", "impact_summary", "recommendation", "notes"]
    ordering_fields = ["id", "title", "severity", "status", "due_date", "created_at"]


class NonConformityViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = NonConformity.objects.select_related(
        "organization",
        "audit_finding",
        "related_assessment",
        "related_requirement",
        "related_control",
    ).all()
    serializer_class = NonConformitySerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "owner_name", "root_cause", "containment_action", "remediation_expectation", "verification_notes"]
    ordering_fields = ["id", "title", "severity", "status", "due_date", "created_at"]


class CorrectiveActionViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = CorrectiveAction.objects.select_related(
        "organization",
        "related_finding",
        "related_non_conformity",
        "related_assessment",
        "related_control",
        "related_infrastructure",
    ).all()
    serializer_class = CorrectiveActionSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "owner_name", "action_summary", "success_metric", "blocker_summary", "verification_notes"]
    ordering_fields = ["id", "title", "priority", "status", "start_date", "due_date", "completed_date", "created_at"]


class AssetInventoryItemViewSet(SpatialDatasetViewSetMixin, OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = AssetInventoryItem.objects.select_related("organization", "owner_stakeholder", "related_infrastructure", "sector_ref").all()
    serializer_class = AssetInventoryItemSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["code", "name", "asset_type", "sector", "sector_ref__name", "owner_name", "essential_function", "admin_area", "location", "summary"]
    ordering_fields = ["id", "code", "name", "asset_type", "criticality_level", "status", "created_at"]


class ThreatEventViewSet(SpatialDatasetViewSetMixin, OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = ThreatEvent.objects.select_related("organization", "reporting_stakeholder", "related_infrastructure", "asset_item").all()
    serializer_class = ThreatEventSerializer
    permission_classes = [IsAuthenticated]
    search_fields = [
        "title",
        "threat_type",
        "threat_source_type",
        "status",
        "suspected_actor",
        "summary",
        "recommended_action",
        "admin_area",
        "location",
    ]
    ordering_fields = ["id", "title", "status", "severity", "confidence_level", "first_seen_at", "last_seen_at", "created_at"]


class VulnerabilityRecordViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = VulnerabilityRecord.objects.select_related("organization", "related_infrastructure", "asset_item", "related_threat_event").all()
    serializer_class = VulnerabilityRecordSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "vulnerability_type", "owner_name", "summary", "remediation_guidance", "notes"]
    ordering_fields = ["id", "title", "status", "severity", "exploitability_level", "discovered_on", "remediation_due_date", "created_at"]


class RiskScenarioViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = RiskScenario.objects.select_related(
        "organization",
        "risk_register_entry",
        "related_infrastructure",
        "asset_item",
        "related_threat_event",
        "vulnerability_record",
    ).all()
    serializer_class = RiskScenarioSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "scenario_owner", "scenario_summary", "business_impact", "response_plan", "notes"]
    ordering_fields = ["id", "title", "status", "risk_level", "treatment_status", "risk_score", "review_due_date", "created_at"]


class RiskAssessmentReviewViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = RiskAssessmentReview.objects.select_related("organization", "risk_scenario", "risk_register_entry", "reviewer_stakeholder").all()
    serializer_class = RiskAssessmentReviewSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "summary", "recommendations", "notes"]
    ordering_fields = ["id", "title", "status", "review_date", "follow_up_date", "residual_risk_level", "created_at"]


class ThreatBulletinViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = ThreatBulletin.objects.select_related("organization", "related_threat_event", "related_infrastructure", "target_sector_ref").all()
    serializer_class = ThreatBulletinSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "bulletin_type", "target_sector", "target_sector_ref__name", "summary", "recommended_actions", "source_reference"]
    ordering_fields = ["id", "title", "status", "severity", "issued_on", "valid_until", "created_at"]


class IndicatorViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Indicator.objects.select_related("organization", "related_bulletin", "related_threat_event").all()
    serializer_class = IndicatorSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "value", "indicator_type", "status", "notes"]
    ordering_fields = ["id", "title", "indicator_type", "status", "first_seen_at", "last_seen_at", "created_at"]


class DistributionGroupViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = DistributionGroup.objects.select_related("organization", "target_sector_ref").prefetch_related("stakeholders").all()
    serializer_class = DistributionGroupSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "group_type", "target_sector", "target_sector_ref__name", "distribution_notes", "stakeholders__name"]
    ordering_fields = ["id", "title", "group_type", "status", "created_at"]


class InformationShareViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = InformationShare.objects.select_related(
        "organization",
        "related_bulletin",
        "related_threat_event",
        "distribution_group",
        "target_stakeholder",
    ).all()
    serializer_class = InformationShareSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "share_channel", "status", "message_summary", "action_requested", "access_link"]
    ordering_fields = ["id", "title", "status", "share_channel", "shared_at", "acknowledgement_due_date", "created_at"]


class AcknowledgementViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Acknowledgement.objects.select_related("organization", "information_share", "stakeholder").all()
    serializer_class = AcknowledgementSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["information_share__title", "stakeholder__name", "action_note", "notes"]
    ordering_fields = ["id", "status", "responded_at", "created_at"]


def build_download_filename(document):
    safe_title = "".join(character if character.isalnum() or character in {"-", "_"} else "_" for character in (document.title or "generated_document"))
    extension = {
        "markdown": "md",
        "text": "txt",
        "json": "json",
        "pdf": "pdf",
        "docx": "docx",
    }.get(document.output_format, "txt")
    return f"{safe_title}_{document.version_label or f'v{document.version_number}'}.{extension}"


class GeneratedDocumentViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = GeneratedDocument.objects.select_related("organization").all()
    serializer_class = GeneratedDocumentSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "module_key", "module_label", "record_title", "summary", "generated_by_name", "approved_by_name", "status"]
    ordering_fields = ["id", "title", "status", "generated_on", "published_on", "version_number", "created_at"]

    @action(detail=False, methods=["post"], url_path="generate-report")
    def generate_report(self, request):
        request_serializer = GenerateReportDocumentSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        user = request.user
        organization = getattr(user, "organization", None)
        if organization is None:
            return Response({"detail": "A workspace organization is required to generate documents."}, status=400)

        validated = request_serializer.validated_data
        module_key = validated["module_key"]
        module_label = validated.get("module_label") or module_key.replace("_", " ").replace("-", " ").title()
        document_type = validated["document_type"]
        output_format = validated["output_format"]
        record_id = validated.get("record_id")
        record_title = validated.get("record_title", "")
        rows = validated["rows"]
        report_preset = validated.get("report_preset", "")
        search_term = validated.get("search", "")

        version_number = (
            self.get_queryset()
            .filter(module_key=module_key, record_id=record_id, document_type=document_type)
            .count()
            + 1
        )
        version_label = f"v{version_number}"
        title = validated.get("title") or f"{module_label} {document_type.replace('_', ' ')} {version_label}"
        try:
            payload = build_document_payload(
                title=title,
                module_label=module_label,
                report_preset=report_preset,
                document_type=document_type,
                output_format=output_format,
                rows=rows,
                search_term=search_term,
            )
        except RuntimeError as exc:
            return Response({"detail": str(exc)}, status=400)
        filename = build_download_filename(
            type(
                "GeneratedName",
                (),
                {"title": title, "version_label": version_label, "version_number": version_number, "output_format": output_format},
            )()
        )

        document = GeneratedDocument.objects.create(
            organization=organization,
            title=title,
            module_key=module_key,
            module_label=module_label,
            record_id=record_id,
            record_title=record_title,
            document_type=document_type,
            output_format=output_format,
            version_number=version_number,
            version_label=version_label,
            generated_by_name=user.get_full_name() or user.email,
            summary=build_document_summary(module_label, len(rows), document_type, search_term),
            content_text=payload["content_text"],
            mime_type=payload["mime_type"],
            file_size_bytes=len(payload["file_bytes"]),
            source_snapshot={
                "report_preset": report_preset,
                "rows": rows,
                "columns": validated.get("columns", []),
                "search": search_term,
            },
            created_by=user,
            updated_by=user,
        )
        document.generated_file.save(filename, ContentFile(payload["file_bytes"]), save=False)
        document.save(update_fields=["generated_file", "mime_type", "file_size_bytes", "updated_at"])

        serializer = self.get_serializer(document)
        return Response(serializer.data, status=201)

    @action(detail=True, methods=["get"], url_path="download")
    def download(self, request, pk=None):
        document = self.get_object()
        content_type = document.mime_type or TEXT_CONTENT_TYPES.get(document.output_format, "text/plain; charset=utf-8")
        payload = document.content_text or ""
        if document.generated_file:
            document.generated_file.open("rb")
            payload = document.generated_file.read()
            document.generated_file.close()

        response = HttpResponse(payload, content_type=content_type)
        response["Content-Disposition"] = f'attachment; filename="{build_download_filename(document)}"'
        return response


class ReviewCycleViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = ReviewCycle.objects.select_related("organization", "generated_document").all()
    serializer_class = ReviewCycleSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "module_key", "module_label", "record_title", "owner_name", "scope_summary", "notes"]
    ordering_fields = ["id", "title", "status", "last_review_date", "next_review_date", "created_at"]


class ReviewRecordViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = ReviewRecord.objects.select_related("organization", "review_cycle", "generated_document").all()
    serializer_class = ReviewRecordSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "reviewer_name", "summary", "recommendations", "notes"]
    ordering_fields = ["id", "title", "status", "decision", "review_date", "next_review_date", "created_at"]


class ChangeLogEntryViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = ChangeLogEntry.objects.select_related("organization", "generated_document", "review_cycle", "review_record").all()
    serializer_class = ChangeLogEntrySerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "module_key", "module_label", "record_title", "change_type", "summary", "changed_by_name"]
    ordering_fields = ["id", "title", "change_type", "changed_on", "created_at"]


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
