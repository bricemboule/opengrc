from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.org.models import Organization

from ...models import (
    ActionPlanTask,
    AuditFramework,
    AvailabilityStatus,
    CapacityAssessment,
    ConsultationType,
    ContingencyPlan,
    CyberStandard,
    DeliverableCategory,
    DeliverableMilestone,
    DeliveryMode,
    DeskStudyReview,
    DeskStudySourceType,
    EmergencyAssetType,
    EmergencyResponseAsset,
    ExerciseType,
    Phase,
    PlanType,
    PriorityLevel,
    RiskRegisterEntry,
    RiskTreatmentStatus,
    SimulationExercise,
    StandardType,
    StakeholderConsultation,
    TrainingProgram,
    TrainingType,
    WorkflowStatus,
)

DEMO_ORG_CODE = "opengrc-pagination-demo"
TARGET_COUNTS = {
    "risk_register_entries": 12,
    "capacity_assessments": 13,
    "training_programs": 5,
    "contingency_plans": 6,
    "emergency_response_assets": 7,
    "simulation_exercises": 11,
    "cyber_standards": 4,
    "audit_frameworks": 10,
    "deliverable_milestones": 21,
    "desk_study_reviews": 8,
    "stakeholder_consultations": 9,
    "action_plan_tasks": 14,
}


class Command(BaseCommand):
    help = "Populate cyber GRC modules with mixed totals for pagination and workflow testing."

    def add_arguments(self, parser):
        parser.add_argument("--organization-id", type=int, help="Target a specific organization id.")
        parser.add_argument(
            "--replace-existing",
            action="store_true",
            help="Delete existing records in the targeted cyber GRC modules for the selected organization before seeding exact demo totals.",
        )

    def resolve_organization(self, organization_id):
        if organization_id:
            organization = Organization.objects.filter(id=organization_id).first()
            if not organization:
                raise CommandError(f"Organization {organization_id} was not found.")
            return organization

        organization = Organization.objects.order_by("id").first()
        if organization:
            return organization

        return Organization.objects.create(
            name="OpenGRC Pagination Demo",
            code=DEMO_ORG_CODE,
            email="demo@opengrc.local",
            description="Demo organization for cyber GRC pagination testing.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        organization_id = options.get("organization_id")
        replace_existing = options.get("replace_existing", False)
        if replace_existing and not organization_id:
            raise CommandError("--replace-existing requires --organization-id to avoid wiping the wrong organization.")

        organization = self.resolve_organization(organization_id)
        today = timezone.localdate()

        if replace_existing:
            self.stdout.write(self.style.WARNING(f"Replacing targeted cyber GRC records for organization {organization.id} ({organization.name})."))
            for model in [
                ActionPlanTask,
                DeliverableMilestone,
                AuditFramework,
                CyberStandard,
                SimulationExercise,
                EmergencyResponseAsset,
                ContingencyPlan,
                TrainingProgram,
                CapacityAssessment,
                RiskRegisterEntry,
                StakeholderConsultation,
                DeskStudyReview,
            ]:
                model.objects.filter(organization=organization).delete()

        summary = []
        summary.append(("desk_study_reviews",) + self.ensure_desk_studies(organization, today))
        summary.append(("stakeholder_consultations",) + self.ensure_consultations(organization, today))
        summary.append(("risk_register_entries",) + self.ensure_risk_entries(organization, today))
        summary.append(("capacity_assessments",) + self.ensure_capacity_assessments(organization, today))
        summary.append(("training_programs",) + self.ensure_training_programs(organization))
        summary.append(("contingency_plans",) + self.ensure_contingency_plans(organization, today))
        summary.append(("emergency_response_assets",) + self.ensure_emergency_assets(organization))
        summary.append(("simulation_exercises",) + self.ensure_simulation_exercises(organization, today))
        summary.append(("cyber_standards",) + self.ensure_standards(organization, today))
        summary.append(("audit_frameworks",) + self.ensure_audit_frameworks(organization, today))
        summary.append(("deliverable_milestones",) + self.ensure_deliverables(organization, today))
        summary.append(("action_plan_tasks",) + self.ensure_action_plan_tasks(organization, today))

        for label, target, total, created in summary:
            warning = ""
            if total != target:
                warning = f" (target {target}, total {total}; existing non-demo data may already exceed the demo target)"
            self.stdout.write(f"- {label}: created {created}, total {total}{warning}")

        self.stdout.write(self.style.SUCCESS("Cyber GRC workflow demo data is ready."))

    def ensure_desk_studies(self, organization, today):
        return self.ensure_title_records(
            DeskStudyReview,
            organization,
            TARGET_COUNTS["desk_study_reviews"],
            lambda index, title: {
                "title": title,
                "source_type": [
                    DeskStudySourceType.POLICY,
                    DeskStudySourceType.REPORT,
                    DeskStudySourceType.REGULATION,
                    DeskStudySourceType.STANDARD,
                    DeskStudySourceType.INCIDENT,
                    DeskStudySourceType.LEGAL,
                ][((index - 1) % 6)],
                "document_owner": f"Desk Review Owner {index:02d}",
                "scope": ["Legal baseline", "Institutional mapping", "Sector readiness", "Risk evidence"][((index - 1) % 4)],
                "summary": f"Desk study summary {index:02d}.",
                "gap_summary": "Generated by seed_pagination_demo." if index % 4 != 0 else "",
                "recommendation_summary": "Generated by seed_pagination_demo." if index % 3 != 0 else "",
                "priority": [PriorityLevel.MEDIUM, PriorityLevel.HIGH, PriorityLevel.CRITICAL][((index - 1) % 3)],
                "status": [WorkflowStatus.PLANNED, WorkflowStatus.IN_PROGRESS, WorkflowStatus.IN_REVIEW, WorkflowStatus.VALIDATED][((index - 1) % 4)],
                "due_date": today + timedelta(days=index * 6),
                "completed_date": today - timedelta(days=index) if index % 5 == 0 else None,
                "next_action": f"Desk study next action {index:02d}.",
                "notes": "Generated by seed_pagination_demo.",
            },
            prefix="Pagination Demo Desk Study",
        )

    def ensure_consultations(self, organization, today):
        return self.ensure_title_records(
            StakeholderConsultation,
            organization,
            TARGET_COUNTS["stakeholder_consultations"],
            lambda index, title: {
                "title": title,
                "consultation_type": [
                    ConsultationType.BRIEFING,
                    ConsultationType.INTERVIEW,
                    ConsultationType.WORKSHOP,
                    ConsultationType.VALIDATION,
                    ConsultationType.FIELD_VISIT,
                ][((index - 1) % 5)],
                "objective": f"Consultation objective {index:02d}.",
                "planned_date": today + timedelta(days=index * 8),
                "completed_date": today - timedelta(days=index) if index % 4 == 0 else None,
                "status": [WorkflowStatus.PLANNED, WorkflowStatus.IN_PROGRESS, WorkflowStatus.COMPLETED][((index - 1) % 3)],
                "focal_person": f"Consultation Lead {index:02d}",
                "outcome_summary": "Generated by seed_pagination_demo." if index % 2 == 0 else "",
                "follow_up_actions": f"Follow-up actions {index:02d}.",
                "next_follow_up_date": today + timedelta(days=index * 10),
                "notes": "Generated by seed_pagination_demo.",
            },
            prefix="Pagination Demo Consultation",
        )

    def ensure_risk_entries(self, organization, today):
        return self.ensure_title_records(
            RiskRegisterEntry,
            organization,
            TARGET_COUNTS["risk_register_entries"],
            lambda index, title: {
                "title": title,
                "category": ["Governance", "Operations", "Network", "Vendor"][((index - 1) % 4)],
                "scenario": f"Demo risk scenario {index} for pagination testing.",
                "likelihood": (index % 5) + 1,
                "impact": ((index + 1) % 5) + 1,
                "risk_score": f"{((index % 5) + 1) * (((index + 1) % 5) + 1):.2f}",
                "risk_level": [PriorityLevel.LOW, PriorityLevel.MEDIUM, PriorityLevel.HIGH, PriorityLevel.CRITICAL][((index - 1) % 4)],
                "treatment_status": [
                    RiskTreatmentStatus.IDENTIFIED,
                    RiskTreatmentStatus.ASSESSING,
                    RiskTreatmentStatus.MITIGATING,
                    RiskTreatmentStatus.ACCEPTED,
                    RiskTreatmentStatus.CLOSED,
                ][((index - 1) % 5)],
                "risk_owner": f"Risk Owner {index:02d}",
                "response_plan": f"Demo response plan {index:02d}.",
                "response_deadline": today + timedelta(days=index * 5),
                "last_reviewed_at": today - timedelta(days=index),
                "update_notes": "Generated by seed_pagination_demo.",
            },
            prefix="Pagination Demo Risk",
        )

    def ensure_capacity_assessments(self, organization, today):
        return self.ensure_title_records(
            CapacityAssessment,
            organization,
            TARGET_COUNTS["capacity_assessments"],
            lambda index, title: {
                "title": title,
                "scope": ["National", "Sector", "Institution", "Service"][((index - 1) % 4)],
                "assessment_area": ["Governance", "Detection", "Response", "Recovery", "Awareness"][((index - 1) % 5)],
                "current_maturity": ((index - 1) % 4) + 1,
                "target_maturity": 4 if index % 2 == 0 else 5,
                "gap_level": [PriorityLevel.MEDIUM, PriorityLevel.HIGH, PriorityLevel.CRITICAL][((index - 1) % 3)],
                "status": [WorkflowStatus.PLANNED, WorkflowStatus.IN_PROGRESS, WorkflowStatus.IN_REVIEW, WorkflowStatus.VALIDATED][((index - 1) % 4)],
                "lead_assessor": f"Capacity Assessor {index:02d}",
                "due_date": today + timedelta(days=index * 9),
                "completed_date": today - timedelta(days=index) if index % 6 == 0 else None,
                "baseline_summary": f"Baseline summary {index:02d}.",
                "gap_summary": f"Gap summary {index:02d}.",
                "priority_actions": f"Priority actions {index:02d}.",
                "notes": "Generated by seed_pagination_demo.",
            },
            prefix="Pagination Demo Capacity",
        )

    def ensure_training_programs(self, organization):
        return self.ensure_title_records(
            TrainingProgram,
            organization,
            TARGET_COUNTS["training_programs"],
            lambda index, title: {
                "title": title,
                "program_type": [
                    TrainingType.RISK_MANAGEMENT,
                    TrainingType.CONTINGENCY_RESPONSE,
                    TrainingType.AUDIT_AWARENESS,
                    TrainingType.STANDARDS_COMPLIANCE,
                    TrainingType.STAKEHOLDER_ENGAGEMENT,
                ][((index - 1) % 5)],
                "target_audience": ["Executives", "CERT teams", "Sector regulators", "Operators", "PMO"][((index - 1) % 5)],
                "duration_days": (index % 4) + 1,
                "delivery_mode": [DeliveryMode.IN_PERSON, DeliveryMode.HYBRID, DeliveryMode.VIRTUAL][((index - 1) % 3)],
                "status": [WorkflowStatus.PLANNED, WorkflowStatus.IN_PROGRESS, WorkflowStatus.COMPLETED][((index - 1) % 3)],
                "certificate_required": index % 2 == 0,
                "participant_target": 15 + index * 4,
                "summary": "Generated by seed_pagination_demo.",
            },
            prefix="Pagination Demo Training",
        )

    def ensure_contingency_plans(self, organization, today):
        return self.ensure_title_records(
            ContingencyPlan,
            organization,
            TARGET_COUNTS["contingency_plans"],
            lambda index, title: {
                "title": title,
                "plan_type": [PlanType.NATIONAL, PlanType.SECTORAL, PlanType.INCIDENT, PlanType.RECOVERY, PlanType.COMMUNICATION][((index - 1) % 5)],
                "scope": ["National coordination", "Financial services", "Telecom backbone", "Recovery operations", "Executive comms"][((index - 1) % 5)],
                "status": [WorkflowStatus.DRAFT, WorkflowStatus.IN_REVIEW, WorkflowStatus.VALIDATED, WorkflowStatus.ACTIVE][((index - 1) % 4)],
                "communication_procedure": f"Communication procedure {index:02d}.",
                "coordination_mechanism": f"Coordination mechanism {index:02d}.",
                "information_sharing_protocol": f"Sharing protocol {index:02d}.",
                "activation_trigger": f"Activation trigger {index:02d}.",
                "review_cycle": ["Quarterly", "Biannual", "Annual"][((index - 1) % 3)],
                "next_review_date": today + timedelta(days=index * 21),
                "notes": "Generated by seed_pagination_demo.",
            },
            prefix="Pagination Demo Contingency",
        )

    def ensure_emergency_assets(self, organization):
        return self.ensure_named_records(
            EmergencyResponseAsset,
            organization,
            TARGET_COUNTS["emergency_response_assets"],
            lambda index, name: {
                "name": name,
                "asset_type": [EmergencyAssetType.DIGITAL, EmergencyAssetType.PHYSICAL, EmergencyAssetType.FACILITY, EmergencyAssetType.TEAM, EmergencyAssetType.PLATFORM][((index - 1) % 5)],
                "priority": [PriorityLevel.MEDIUM, PriorityLevel.HIGH, PriorityLevel.CRITICAL][((index - 1) % 3)],
                "owner_name": f"Asset Owner {index:02d}",
                "availability_status": [AvailabilityStatus.PLANNED, AvailabilityStatus.READY, AvailabilityStatus.CONSTRAINED, AvailabilityStatus.UNAVAILABLE][((index - 1) % 4)],
                "location": ["Banjul", "Kanifing", "Brikama", "Farafenni"][((index - 1) % 4)],
                "activation_notes": "Generated by seed_pagination_demo.",
            },
            prefix="Pagination Demo Asset",
        )

    def ensure_simulation_exercises(self, organization, today):
        return self.ensure_title_records(
            SimulationExercise,
            organization,
            TARGET_COUNTS["simulation_exercises"],
            lambda index, title: {
                "title": title,
                "exercise_type": [ExerciseType.TABLETOP, ExerciseType.SIMULATION, ExerciseType.LIVE_DRILL][((index - 1) % 3)],
                "planned_date": today + timedelta(days=index * 14),
                "completed_date": today - timedelta(days=index) if index % 4 == 0 else None,
                "status": [WorkflowStatus.PLANNED, WorkflowStatus.IN_PROGRESS, WorkflowStatus.COMPLETED][((index - 1) % 3)],
                "scenario": f"Exercise scenario {index:02d}.",
                "participating_sectors": "Finance, telecom, energy",
                "findings": "Generated by seed_pagination_demo.",
                "lessons_learned": "Generated by seed_pagination_demo.",
            },
            prefix="Pagination Demo Exercise",
        )

    def ensure_standards(self, organization, today):
        return self.ensure_title_records(
            CyberStandard,
            organization,
            TARGET_COUNTS["cyber_standards"],
            lambda index, title: {
                "title": title,
                "standard_type": [
                    StandardType.ISP_EQUIPMENT,
                    StandardType.BANKING_EQUIPMENT,
                    StandardType.CNI_PROTECTION,
                    StandardType.PRIVACY,
                    StandardType.CONFORMITY,
                ][((index - 1) % 5)],
                "target_sector": ["Telecom", "Banking", "Government", "Energy"][((index - 1) % 4)],
                "status": [WorkflowStatus.DRAFT, WorkflowStatus.IN_REVIEW, WorkflowStatus.VALIDATED, WorkflowStatus.ACTIVE][((index - 1) % 4)],
                "version": f"v{index}.0",
                "control_focus": f"Control focus {index:02d}.",
                "review_cycle": ["Quarterly", "Annual"][((index - 1) % 2)],
                "owner_name": f"Standards Owner {index:02d}",
                "summary": "Generated by seed_pagination_demo.",
                "next_review_date": today + timedelta(days=index * 30),
            },
            prefix="Pagination Demo Standard",
        )

    def ensure_audit_frameworks(self, organization, today):
        return self.ensure_title_records(
            AuditFramework,
            organization,
            TARGET_COUNTS["audit_frameworks"],
            lambda index, title: {
                "title": title,
                "scope": ["Sector audit", "Operator audit", "Programme audit", "Control review"][((index - 1) % 4)],
                "status": [WorkflowStatus.DRAFT, WorkflowStatus.SUBMITTED, WorkflowStatus.VALIDATED, WorkflowStatus.ACTIVE][((index - 1) % 4)],
                "audit_frequency": ["Monthly", "Quarterly", "Biannual", "Annual"][((index - 1) % 4)],
                "compliance_focus": f"Compliance focus {index:02d}.",
                "incident_response_procedure": f"Incident response procedure {index:02d}.",
                "recovery_procedure": f"Recovery procedure {index:02d}.",
                "next_review_date": today + timedelta(days=index * 18),
                "review_notes": "Generated by seed_pagination_demo.",
            },
            prefix="Pagination Demo Audit",
        )

    def ensure_deliverables(self, organization, today):
        return self.ensure_title_records(
            DeliverableMilestone,
            organization,
            TARGET_COUNTS["deliverable_milestones"],
            lambda index, title: {
                "title": title,
                "phase": [Phase.RISK, Phase.CONTINGENCY, Phase.STANDARDS, Phase.AUDIT][((index - 1) % 4)],
                "deliverable_category": [
                    DeliverableCategory.RISK_REGISTER,
                    DeliverableCategory.CONTINGENCY,
                    DeliverableCategory.STANDARD,
                    DeliverableCategory.AUDIT,
                    DeliverableCategory.REPORT,
                ][((index - 1) % 5)],
                "status": [WorkflowStatus.DRAFT, WorkflowStatus.PLANNED, WorkflowStatus.IN_PROGRESS, WorkflowStatus.VALIDATED][((index - 1) % 4)],
                "planned_week": index,
                "due_date": today + timedelta(days=index * 7),
                "owner_name": f"Delivery Owner {index:02d}",
                "notes": "Generated by seed_pagination_demo.",
            },
            prefix="Pagination Demo Deliverable",
        )

    def ensure_action_plan_tasks(self, organization, today):
        return self.ensure_title_records(
            ActionPlanTask,
            organization,
            TARGET_COUNTS["action_plan_tasks"],
            lambda index, title: {
                "title": title,
                "workstream": ["Governance", "Mapping", "Capacity", "Response", "Audit"][((index - 1) % 5)],
                "owner_name": f"Action Owner {index:02d}",
                "priority": [PriorityLevel.MEDIUM, PriorityLevel.HIGH, PriorityLevel.CRITICAL][((index - 1) % 3)],
                "status": [WorkflowStatus.PLANNED, WorkflowStatus.IN_PROGRESS, WorkflowStatus.IN_REVIEW, WorkflowStatus.COMPLETED][((index - 1) % 4)],
                "start_date": today - timedelta(days=index),
                "due_date": today + timedelta(days=index * 4),
                "completed_date": today - timedelta(days=index) if index % 5 == 0 else None,
                "success_metric": f"Success metric {index:02d}",
                "blocker_summary": "Dependency still pending." if index % 4 == 0 else "",
                "progress_note": f"Progress note {index:02d}",
                "next_step": f"Next step {index:02d}",
                "notes": "Generated by seed_pagination_demo.",
            },
            prefix="Pagination Demo Action",
        )

    def ensure_title_records(self, model, organization, target_count, defaults_builder, prefix):
        created = 0
        for index in range(1, target_count + 1):
            title = f"{prefix} {index:02d}"
            _, was_created = model.objects.get_or_create(
                organization=organization,
                title=title,
                defaults=defaults_builder(index, title),
            )
            created += int(was_created)
        total = model.objects.filter(organization=organization).count()
        return target_count, total, created

    def ensure_named_records(self, model, organization, target_count, defaults_builder, prefix):
        created = 0
        for index in range(1, target_count + 1):
            name = f"{prefix} {index:02d}"
            _, was_created = model.objects.get_or_create(
                organization=organization,
                name=name,
                defaults=defaults_builder(index, name),
            )
            created += int(was_created)
        total = model.objects.filter(organization=organization).count()
        return target_count, total, created