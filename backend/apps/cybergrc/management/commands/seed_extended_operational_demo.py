from datetime import datetime, time, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.cybergrc.document_generation import build_document_payload
from apps.cybergrc.models import (
    Acknowledgement,
    AcknowledgementStatus,
    AssetInventoryItem,
    AssetInventoryType,
    AuditChecklist,
    AuditFinding,
    AuditFramework,
    AuditPlan,
    AvailabilityStatus,
    BulletinType,
    ChangeLogEntry,
    ChangeType,
    ChecklistStatus,
    ConformityAssessment,
    ConformityLevel,
    ContingencyPlan,
    ControlEvidence,
    CorrectiveAction,
    CriticalInfrastructure,
    CyberStandard,
    DistributionGroup,
    DistributionGroupType,
    DocumentStatus,
    DocumentType,
    EmergencyResponseAsset,
    EvidenceStatus,
    EvidenceType,
    FindingStatus,
    InformationShare,
    Indicator,
    IndicatorStatus,
    IndicatorType,
    NonConformity,
    NonConformityStatus,
    PriorityLevel,
    RequirementType,
    ReviewCycle,
    ReviewCycleStatus,
    ReviewDecision,
    ReviewRecord,
    RiskAssessmentReview,
    RiskRegisterEntry,
    RiskReviewDecision,
    RiskScenario,
    RiskTreatmentStatus,
    Sector,
    ShareChannel,
    ShareStatus,
    Stakeholder,
    StandardControl,
    StandardRequirement,
    ThreatBulletin,
    ThreatEvent,
    ThreatEventStatus,
    ThreatSourceType,
    ThreatType,
    VulnerabilityRecord,
    VulnerabilityStatus,
    WorkflowStatus,
)
from apps.cybergrc.spatial import sync_point_geometry
from apps.incident_management.models import (
    AllocationStatus,
    AssetAllocation,
    AttachmentType,
    CommunicationChannel,
    CommunicationDirection,
    Incident,
    IncidentAssignment,
    IncidentAssignmentStatus,
    IncidentAttachment,
    IncidentCommunication,
    IncidentSeverity,
    IncidentSource,
    IncidentStatus,
    IncidentTask,
    IncidentTaskStatus,
    IncidentType,
    IncidentUpdate,
    IncidentUpdateType,
    SOPExecution,
    SOPExecutionStatus,
    SOPExecutionStep,
    SOPExecutionStepStatus,
    SOPStep,
    SOPStepType,
    SOPTemplate,
    SOPTemplateStatus,
)
from apps.org.models import Organization


class Command(BaseCommand):
    help = "Populate the extended operational modules with realistic demo data."

    def add_arguments(self, parser):
        parser.add_argument("--organization-id", type=int, default=1, help="Organization id to populate.")

    def pick(self, items, index, fallback=None):
        if not items:
            return fallback
        return items[index % len(items)]

    def upsert(self, model, lookup, defaults):
        return model.objects.update_or_create(**lookup, defaults=defaults)

    def fallback_coordinate_pair(self, index):
        coordinates = [
            (Decimal("13.454876"), Decimal("-16.579032")),
            (Decimal("13.443210"), Decimal("-16.673190")),
            (Decimal("13.405500"), Decimal("-16.694120")),
            (Decimal("13.476230"), Decimal("-16.577340")),
            (Decimal("13.433333"), Decimal("-15.533333")),
            (Decimal("13.566667"), Decimal("-15.600000")),
        ]
        return coordinates[index % len(coordinates)]

    def derive_asset_coordinates(self, asset, index):
        infrastructure = getattr(asset, "infrastructure", None)
        base_latitude = getattr(infrastructure, "latitude", None)
        base_longitude = getattr(infrastructure, "longitude", None)

        if base_latitude is None or base_longitude is None:
            base_latitude, base_longitude = self.fallback_coordinate_pair(index)

        offset_seed = ((index % 5) - 2) * Decimal("0.0012")
        offset_partner = (((index + 2) % 5) - 2) * Decimal("0.0009")
        return (
            Decimal(str(base_latitude)) + offset_seed,
            Decimal(str(base_longitude)) + offset_partner,
        )

    def sync_geometry_for_existing_records(self, organization):
        for infrastructure in self.infrastructure:
            if infrastructure.latitude is not None and infrastructure.longitude is not None:
                sync_point_geometry(infrastructure)
                infrastructure.save(update_fields=["geometry_geojson", "updated_at"])

        for asset in EmergencyResponseAsset.objects.filter(organization=organization):
            changed = False
            if asset.capacity_units is None:
                asset.capacity_units = 1 + (asset.id % 4)
                changed = True
            if not asset.last_readiness_check:
                asset.last_readiness_check = self.today - timedelta(days=(asset.id % 30))
                changed = True
            if not asset.deployment_status:
                asset.deployment_status = self.pick(
                    ["idle", "staged", "deployed", "maintenance"],
                    asset.id,
                    "idle",
                )
                changed = True
            if asset.latitude is None or asset.longitude is None:
                latitude, longitude = self.derive_asset_coordinates(asset, asset.id)
                asset.latitude = latitude
                asset.longitude = longitude
                changed = True
            if not asset.location and getattr(asset, "infrastructure", None):
                asset.location = asset.infrastructure.location
                changed = True
            if asset.latitude is not None and asset.longitude is not None:
                sync_point_geometry(asset)
                changed = True
            if changed:
                asset.save()

    def build_document_record(
        self,
        *,
        title,
        module_key,
        module_label,
        document_type,
        output_format,
        rows,
        record_id=None,
        record_title="",
        generated_by_name="OpenGRC Demo Seeder",
    ):
        payload = build_document_payload(
            title=title,
            module_label=module_label,
            report_preset="report",
            document_type=document_type,
            output_format=output_format,
            rows=rows,
            search_term="",
        )

        document, _ = self.upsert(
            self.generated_document_model,
            {"organization": self.organization, "title": title},
            {
                "module_key": module_key,
                "module_label": module_label,
                "record_id": record_id,
                "record_title": record_title,
                "document_type": document_type,
                "output_format": output_format,
                "status": DocumentStatus.APPROVED,
                "version_number": 1,
                "published_on": self.now - timedelta(days=1),
                "generated_by_name": generated_by_name,
                "approved_by_name": "National Cyber Steering Committee",
                "summary": f"{module_label} generated operational export.",
                "content_text": payload["content_text"],
                "mime_type": payload["mime_type"],
                "file_size_bytes": len(payload["file_bytes"]),
                "source_snapshot": {
                    "module_key": module_key,
                    "row_count": len(rows),
                    "record_title": record_title,
                },
                "notes": "Generated by seed_extended_operational_demo.",
            },
        )

        filename = f"{title.lower().replace(' ', '-')}.{output_format}"
        if document.generated_file:
            document.generated_file.delete(save=False)
        document.generated_file.save(filename, ContentFile(payload["file_bytes"]), save=False)
        document.save()
        return document

    @transaction.atomic
    def handle(self, *args, **options):
        organization_id = options["organization_id"]
        self.organization = Organization.objects.filter(id=organization_id).first()
        if not self.organization:
            raise CommandError(f"Organization {organization_id} was not found.")

        self.now = timezone.now()
        self.today = timezone.localdate()
        self.user_model = get_user_model()
        self.generated_document_model = __import__(
            "apps.cybergrc.models", fromlist=["GeneratedDocument"]
        ).GeneratedDocument

        self.users = list(self.user_model.objects.order_by("id"))
        self.sectors = list(Sector.objects.filter(organization=self.organization).order_by("id"))
        self.stakeholders = list(Stakeholder.objects.filter(organization=self.organization).order_by("id"))
        self.infrastructure = list(CriticalInfrastructure.objects.filter(organization=self.organization).order_by("id"))
        self.plans = list(ContingencyPlan.objects.filter(organization=self.organization).order_by("id"))
        self.response_assets = list(EmergencyResponseAsset.objects.filter(organization=self.organization).order_by("id"))
        self.standards = list(CyberStandard.objects.filter(organization=self.organization).order_by("id"))
        self.frameworks = list(AuditFramework.objects.filter(organization=self.organization).order_by("id"))
        self.risks = list(RiskRegisterEntry.objects.filter(organization=self.organization).order_by("id"))

        if not self.stakeholders or not self.infrastructure or not self.plans or not self.response_assets or not self.standards or not self.frameworks or not self.risks:
            raise CommandError(
                "The base CyberGRC demo data is incomplete. Seed the core modules first, then rerun this command."
            )

        self.sync_geometry_for_existing_records(self.organization)
        incident_context = self.seed_incident_operations()
        compliance_context = self.seed_compliance()
        intelligence_context = self.seed_intelligence()
        self.seed_documents_and_reviews(
            incident_context=incident_context,
            compliance_context=compliance_context,
            intelligence_context=intelligence_context,
        )

        summary_models = [
            ("incidents", Incident),
            ("incident_updates", IncidentUpdate),
            ("incident_tasks", IncidentTask),
            ("incident_assignments", IncidentAssignment),
            ("incident_communications", IncidentCommunication),
            ("incident_attachments", IncidentAttachment),
            ("sop_templates", SOPTemplate),
            ("sop_steps", SOPStep),
            ("sop_executions", SOPExecution),
            ("sop_execution_steps", SOPExecutionStep),
            ("asset_allocations", AssetAllocation),
            ("standard_requirements", StandardRequirement),
            ("standard_controls", StandardControl),
            ("conformity_assessments", ConformityAssessment),
            ("control_evidence", ControlEvidence),
            ("audit_plans", AuditPlan),
            ("audit_checklists", AuditChecklist),
            ("audit_findings", AuditFinding),
            ("non_conformities", NonConformity),
            ("corrective_actions", CorrectiveAction),
            ("asset_inventory_items", AssetInventoryItem),
            ("threat_events", ThreatEvent),
            ("vulnerability_records", VulnerabilityRecord),
            ("risk_scenarios", RiskScenario),
            ("risk_assessment_reviews", RiskAssessmentReview),
            ("threat_bulletins", ThreatBulletin),
            ("indicators", Indicator),
            ("distribution_groups", DistributionGroup),
            ("information_shares", InformationShare),
            ("acknowledgements", Acknowledgement),
            ("generated_documents", self.generated_document_model),
            ("review_cycles", ReviewCycle),
            ("review_records", ReviewRecord),
            ("change_log_entries", ChangeLogEntry),
        ]

        self.stdout.write(self.style.SUCCESS("Extended operational demo data is ready."))
        for label, model in summary_models:
            total = model.objects.filter(organization=self.organization).count()
            self.stdout.write(f"- {label}: {total}")

        self.stdout.write(
            self.style.WARNING(
                "Reminder: scheduled reminder delivery still depends on Celery running, and outbound emails still require SMTP configuration."
            )
        )

    def seed_incident_operations(self):
        incident_specs = [
            {
                "title": "National power dispatch malware containment",
                "incident_type": IncidentType.MALWARE,
                "severity": IncidentSeverity.CRITICAL,
                "status": IncidentStatus.ACTIVE,
                "source": IncidentSource.MONITORING,
                "lead_idx": 2,
                "sector_indices": [0, 3],
                "infra_indices": [0, 1],
                "plan_idx": 0,
                "hours_ago": 14,
            },
            {
                "title": "Telecom backbone DDoS coordination",
                "incident_type": IncidentType.DDOS,
                "severity": IncidentSeverity.HIGH,
                "status": IncidentStatus.CONTAINED,
                "source": IncidentSource.EXTERNAL_REPORT,
                "lead_idx": 5,
                "sector_indices": [1],
                "infra_indices": [2, 3],
                "plan_idx": 1,
                "hours_ago": 32,
            },
            {
                "title": "Interbank payment switch recovery",
                "incident_type": IncidentType.SERVICE_OUTAGE,
                "severity": IncidentSeverity.CRITICAL,
                "status": IncidentStatus.RECOVERING,
                "source": IncidentSource.INTERNAL_REPORT,
                "lead_idx": 8,
                "sector_indices": [2],
                "infra_indices": [4, 5],
                "plan_idx": 2,
                "hours_ago": 55,
            },
            {
                "title": "Identity platform unauthorized access response",
                "incident_type": IncidentType.UNAUTHORIZED_ACCESS,
                "severity": IncidentSeverity.HIGH,
                "status": IncidentStatus.ASSESSING,
                "source": IncidentSource.THREAT_INTELLIGENCE,
                "lead_idx": 10,
                "sector_indices": [0, 4],
                "infra_indices": [6],
                "plan_idx": 3,
                "hours_ago": 6,
            },
        ]

        incidents = []
        for index, spec in enumerate(incident_specs):
            lead_stakeholder = self.pick(self.stakeholders, spec["lead_idx"])
            incident = self.upsert(
                Incident,
                {"organization": self.organization, "title": spec["title"]},
                {
                    "incident_type": spec["incident_type"],
                    "severity": spec["severity"],
                    "status": spec["status"],
                    "source": spec["source"],
                    "detected_at": self.now - timedelta(hours=spec["hours_ago"] + 1),
                    "reported_at": self.now - timedelta(hours=spec["hours_ago"]),
                    "closed_at": None,
                    "summary": f"{spec['title']} is being coordinated through the national cyber operations workflow.",
                    "operational_objective": "Contain the threat, stabilize priority services, and coordinate national response actions.",
                    "cross_sector_impact": "Potential cascading disruption across public services, telecom, and financial operations.",
                    "decision_log": "National coordination cell activated. Sector focal points notified.",
                    "lessons_learned": "",
                    "external_reference": f"INC-GMB-{index + 1:03d}",
                    "next_update_due": self.now + timedelta(hours=index + 1),
                    "containment_target_at": self.now + timedelta(hours=index + 3),
                    "recovery_target_at": self.now + timedelta(hours=index + 12),
                    "national_significance": spec["severity"] in {IncidentSeverity.CRITICAL, IncidentSeverity.NATIONAL},
                    "incident_coordinator": self.pick(self.users, index),
                    "lead_stakeholder": lead_stakeholder,
                    "linked_plan": self.pick(self.plans, spec["plan_idx"]),
                },
            )[0]
            incident.affected_sectors.set([self.pick(self.sectors, idx) for idx in spec["sector_indices"] if self.sectors])
            incident.affected_infrastructure.set(
                [self.pick(self.infrastructure, idx) for idx in spec["infra_indices"] if self.infrastructure]
            )
            incidents.append(incident)

            update_specs = [
                ("Situation update", IncidentUpdateType.SITUATION, "Coordinating telemetry validation with operators."),
                ("Containment decision", IncidentUpdateType.CONTAINMENT, "Edge filtering and traffic shaping approved."),
                ("Recovery checkpoint", IncidentUpdateType.RECOVERY, "Recovery milestones confirmed with service owners."),
            ]
            for update_index, (title_suffix, update_type, message) in enumerate(update_specs, start=1):
                self.upsert(
                    IncidentUpdate,
                    {
                        "organization": self.organization,
                        "incident": incident,
                        "title": f"{incident.title} - {title_suffix}",
                    },
                    {
                        "update_type": update_type,
                        "message": message,
                        "status_snapshot": incident.status,
                        "severity_snapshot": incident.severity,
                        "recorded_at": incident.reported_at + timedelta(hours=update_index * 2),
                        "next_step": "Confirm execution against sector playbooks.",
                    },
                )

            task_specs = [
                ("Activate cross-sector briefing", IncidentTaskStatus.COMPLETED, IncidentSeverity.HIGH),
                ("Validate network containment measures", IncidentTaskStatus.IN_PROGRESS, IncidentSeverity.CRITICAL),
                ("Prepare executive situation note", IncidentTaskStatus.PLANNED, IncidentSeverity.MEDIUM),
            ]
            incident_tasks = []
            for task_index, (task_title, task_status, priority) in enumerate(task_specs, start=1):
                task = self.upsert(
                    IncidentTask,
                    {
                        "organization": self.organization,
                        "incident": incident,
                        "title": f"{incident.title} - {task_title}",
                    },
                    {
                        "description": f"{task_title} for {incident.title.lower()}.",
                        "status": task_status,
                        "priority": priority,
                        "assigned_to": self.pick(self.users, index + task_index),
                        "due_at": self.now + timedelta(hours=task_index * 4),
                        "completed_at": self.now - timedelta(hours=1) if task_status == IncidentTaskStatus.COMPLETED else None,
                        "blocker_summary": "",
                        "next_step": "Report progress during the next coordination call.",
                    },
                )[0]
                incident_tasks.append(task)

            assignment_specs = [
                ("Sector coordination lead", IncidentAssignmentStatus.ACTIVE),
                ("Technical response lead", IncidentAssignmentStatus.ACKNOWLEDGED),
            ]
            for assign_index, (role_in_response, assignment_status) in enumerate(assignment_specs, start=1):
                self.upsert(
                    IncidentAssignment,
                    {
                        "organization": self.organization,
                        "incident": incident,
                        "role_in_response": role_in_response,
                    },
                    {
                        "assignee": self.pick(self.users, index + assign_index),
                        "stakeholder": self.pick(self.stakeholders, index + assign_index),
                        "status": assignment_status,
                        "assigned_at": incident.reported_at + timedelta(minutes=30 * assign_index),
                        "acknowledged_at": incident.reported_at + timedelta(minutes=50 * assign_index),
                        "released_at": None,
                        "notes": f"{role_in_response} assigned through the incident command workflow.",
                    },
                )

            self.upsert(
                IncidentCommunication,
                {
                    "organization": self.organization,
                    "incident": incident,
                    "subject": f"{incident.title} - stakeholder update",
                },
                {
                    "direction": CommunicationDirection.OUTBOUND,
                    "channel": self.pick(
                        [CommunicationChannel.EMAIL, CommunicationChannel.BRIEFING, CommunicationChannel.VIDEO],
                        index,
                        CommunicationChannel.EMAIL,
                    ),
                    "audience": "National cyber steering group",
                    "message": "This operational update summarizes current impact, measures taken, and next coordination steps.",
                    "sent_at": incident.reported_at + timedelta(hours=1),
                    "external_reference": f"COMMS-{index + 1:03d}",
                    "requires_acknowledgement": True,
                },
            )

            self.upsert(
                IncidentAttachment,
                {
                    "organization": self.organization,
                    "incident": incident,
                    "title": f"{incident.title} - evidence bundle",
                },
                {
                    "attachment_type": self.pick(
                        [AttachmentType.LOG, AttachmentType.EVIDENCE, AttachmentType.REPORT, AttachmentType.SCREENSHOT],
                        index,
                        AttachmentType.EVIDENCE,
                    ),
                    "reference_url": f"https://docs.opengrc.local/incidents/{index + 1}/evidence",
                    "reference_label": "Operational evidence bundle",
                    "notes": "Linked evidence for the command center and review trail.",
                },
            )

            template = self.upsert(
                SOPTemplate,
                {"organization": self.organization, "code": f"SOP-IR-{index + 1:03d}"},
                {
                    "contingency_plan": self.pick(self.plans, spec["plan_idx"]),
                    "related_artifact": None,
                    "related_infrastructure": self.pick(self.infrastructure, spec["infra_indices"][0]),
                    "owner_stakeholder": lead_stakeholder,
                    "title": f"{incident.title} response playbook",
                    "version": "v1.0",
                    "status": SOPTemplateStatus.ACTIVE,
                    "objective": "Provide an executable response flow for sector coordination, containment, and service stabilization.",
                    "activation_trigger": "Activate when incident severity reaches high or above.",
                    "review_notes": "Aligned with contingency planning and response governance.",
                    "last_reviewed_at": self.today - timedelta(days=14 + index),
                    "notes": "Generated by seed_extended_operational_demo.",
                },
            )[0]

            step_specs = [
                ("Trigger stakeholder escalation", SOPStepType.ESCALATION, True, "National coordinator", 20),
                ("Validate service impact and telemetry", SOPStepType.TECHNICAL, True, "Technical lead", 45),
                ("Issue coordination message", SOPStepType.COMMUNICATION, True, "Communications lead", 25),
                ("Capture evidence and decisions", SOPStepType.EVIDENCE, False, "Documentation lead", 15),
            ]
            for step_order, (step_title, step_type, required, responsible_role, minutes) in enumerate(step_specs, start=1):
                self.upsert(
                    SOPStep,
                    {
                        "organization": self.organization,
                        "template": template,
                        "step_order": step_order,
                    },
                    {
                        "title": step_title,
                        "instruction": f"{step_title} for {incident.title.lower()}.",
                        "step_type": step_type,
                        "is_required": required,
                        "responsible_role": responsible_role,
                        "default_assignee": self.pick(self.users, index + step_order),
                        "estimated_duration_minutes": minutes,
                        "evidence_hint": "Capture coordination logs, screenshots, or call notes.",
                        "escalation_hint": "Escalate to national level if service degradation widens.",
                    },
                )

            execution = self.upsert(
                SOPExecution,
                {
                    "organization": self.organization,
                    "incident": incident,
                    "template": template,
                    "title": f"{incident.title} execution",
                },
                {
                    "status": self.pick(
                        [SOPExecutionStatus.ACTIVE, SOPExecutionStatus.COMPLETED, SOPExecutionStatus.BLOCKED],
                        index,
                        SOPExecutionStatus.ACTIVE,
                    ),
                    "execution_commander": self.pick(self.users, index),
                    "started_at": incident.reported_at + timedelta(minutes=20),
                    "target_completion_at": incident.reported_at + timedelta(hours=8),
                    "completed_at": self.now - timedelta(hours=2) if index == 1 else None,
                    "summary": "Operational execution of the incident playbook.",
                    "outcome_summary": "Containment and stakeholder coordination actions tracked against the playbook.",
                    "blocker_summary": "" if index != 2 else "Awaiting third-party maintenance confirmation.",
                    "next_action": "Continue execution and capture evidence at each milestone.",
                },
            )[0]

            for template_step in template.steps.order_by("step_order"):
                self.upsert(
                    SOPExecutionStep,
                    {
                        "organization": self.organization,
                        "execution": execution,
                        "step_order": template_step.step_order,
                    },
                    {
                        "template_step": template_step,
                        "title": template_step.title,
                        "instruction": template_step.instruction,
                        "step_type": template_step.step_type,
                        "status": self.pick(
                            [
                                SOPExecutionStepStatus.COMPLETED,
                                SOPExecutionStepStatus.IN_PROGRESS,
                                SOPExecutionStepStatus.PLANNED,
                                SOPExecutionStepStatus.BLOCKED,
                            ],
                            index + template_step.step_order,
                            SOPExecutionStepStatus.PLANNED,
                        ),
                        "is_required": template_step.is_required,
                        "assigned_to": template_step.default_assignee,
                        "completed_by": template_step.default_assignee if template_step.step_order == 1 else None,
                        "started_at": execution.started_at + timedelta(minutes=template_step.step_order * 15),
                        "completed_at": execution.started_at + timedelta(minutes=template_step.step_order * 30)
                        if template_step.step_order == 1
                        else None,
                        "actual_duration_minutes": template_step.estimated_duration_minutes,
                        "evidence_reference": f"https://docs.opengrc.local/sop/{template.id}/step-{template_step.step_order}",
                        "blocker_summary": "" if template_step.step_order != 3 else "Awaiting message clearance.",
                        "notes": "Generated by seed_extended_operational_demo.",
                    },
                )

            for alloc_index in range(2):
                emergency_asset = self.pick(self.response_assets, index * 2 + alloc_index)
                allocation = self.upsert(
                    AssetAllocation,
                    {
                        "organization": self.organization,
                        "incident": incident,
                        "title": f"{incident.title} - allocation {alloc_index + 1}",
                    },
                    {
                        "emergency_asset": emergency_asset,
                        "destination_infrastructure": self.pick(self.infrastructure, spec["infra_indices"][0]),
                        "related_task": self.pick(incident_tasks, alloc_index),
                        "approved_by": self.pick(self.users, index + alloc_index),
                        "requested_by": self.pick(self.users, index + alloc_index + 1),
                        "status": self.pick(
                            [
                                AllocationStatus.APPROVED,
                                AllocationStatus.MOBILIZING,
                                AllocationStatus.DEPLOYED,
                                AllocationStatus.RELEASED,
                            ],
                            index + alloc_index,
                            AllocationStatus.APPROVED,
                        ),
                        "priority": incident.severity,
                        "quantity_requested": 1 + alloc_index,
                        "quantity_allocated": 1 + alloc_index,
                        "requested_at": incident.reported_at + timedelta(minutes=45 + alloc_index * 15),
                        "approved_at": incident.reported_at + timedelta(hours=1, minutes=15 + alloc_index * 10),
                        "mobilized_at": incident.reported_at + timedelta(hours=2, minutes=15),
                        "deployed_at": incident.reported_at + timedelta(hours=4) if alloc_index == 1 else None,
                        "released_at": self.now - timedelta(hours=5) if alloc_index == 0 and index == 1 else None,
                        "destination": self.pick(self.infrastructure, spec["infra_indices"][0]).location,
                        "deployment_notes": "Allocated through the emergency coordination board.",
                        "release_notes": "Released after service stabilization." if alloc_index == 0 and index == 1 else "",
                    },
                )[0]

                emergency_asset.availability_status = self.pick(
                    [AvailabilityStatus.READY, AvailabilityStatus.CONSTRAINED, AvailabilityStatus.UNAVAILABLE],
                    index + alloc_index,
                    AvailabilityStatus.READY,
                )
                emergency_asset.deployment_status = self.pick(
                    ["staged", "deployed", "returning", "maintenance"],
                    index + alloc_index,
                    "staged",
                )
                emergency_asset.capacity_units = max(emergency_asset.capacity_units or 1, allocation.quantity_allocated or 1)
                emergency_asset.last_readiness_check = self.today - timedelta(days=index + alloc_index + 2)
                emergency_asset.save()

        return {"incidents": incidents}

    def seed_compliance(self):
        standards = self.standards[:4]
        frameworks = self.frameworks[:4]
        requirements = []
        controls = []
        assessments = []
        audit_plans = []
        findings = []
        non_conformities = []

        requirement_templates = [
            ("Identity and access governance", RequirementType.GOVERNANCE, PriorityLevel.CRITICAL),
            ("Asset hardening baseline", RequirementType.TECHNICAL, PriorityLevel.HIGH),
            ("Incident reporting obligations", RequirementType.REPORTING, PriorityLevel.MEDIUM),
        ]

        for std_index, standard in enumerate(standards, start=1):
            for req_index, (title, req_type, priority) in enumerate(requirement_templates, start=1):
                requirement = self.upsert(
                    StandardRequirement,
                    {
                        "organization": self.organization,
                        "related_standard": standard,
                        "code": f"{standard.id}-REQ-{req_index:02d}",
                    },
                    {
                        "title": f"{standard.title} - {title}",
                        "chapter": f"Chapter {req_index}",
                        "requirement_type": req_type,
                        "status": self.pick(
                            [WorkflowStatus.ACTIVE, WorkflowStatus.VALIDATED, WorkflowStatus.IN_REVIEW],
                            std_index + req_index,
                            WorkflowStatus.ACTIVE,
                        ),
                        "priority": priority,
                        "implementation_guidance": "Implement sector-approved controls, role ownership, and evidence collection.",
                        "verification_method": "Review documented evidence, interview responsible teams, and inspect operational controls.",
                        "owner_name": self.pick(self.stakeholders, std_index + req_index).name,
                        "sort_order": req_index,
                        "summary": "Seeded operational requirement for compliance testing.",
                        "notes": "Generated by seed_extended_operational_demo.",
                    },
                )[0]
                requirements.append(requirement)

                control = self.upsert(
                    StandardControl,
                    {
                        "organization": self.organization,
                        "related_standard": standard,
                        "code": f"{standard.id}-CTL-{req_index:02d}",
                    },
                    {
                        "related_requirement": requirement,
                        "title": f"{standard.title} - control {req_index}",
                        "domain": self.pick(["Access", "Hardening", "Reporting", "Continuity"], req_index, "Access"),
                        "control_type": self.pick(["preventive", "detective", "corrective"], req_index, "preventive"),
                        "status": WorkflowStatus.ACTIVE,
                        "priority": priority,
                        "control_objective": "Maintain verifiable operational control effectiveness.",
                        "control_procedure": "Run monthly checks, capture evidence, and escalate deviations.",
                        "measurement_criteria": "Evidence currency, owner acknowledgement, and control effectiveness trend.",
                        "owner_name": self.pick(self.stakeholders, std_index + req_index + 3).name,
                        "sort_order": req_index,
                        "notes": "Generated by seed_extended_operational_demo.",
                    },
                )[0]
                controls.append(control)

                assessment = self.upsert(
                    ConformityAssessment,
                    {
                        "organization": self.organization,
                        "title": f"{standard.title} - conformity assessment {req_index}",
                    },
                    {
                        "related_standard": standard,
                        "related_requirement": requirement,
                        "related_control": control,
                        "related_framework": self.pick(frameworks, std_index + req_index),
                        "target_stakeholder": self.pick(self.stakeholders, std_index + req_index + 6),
                        "related_infrastructure": self.pick(self.infrastructure, std_index + req_index),
                        "status": self.pick(
                            [WorkflowStatus.PLANNED, WorkflowStatus.IN_PROGRESS, WorkflowStatus.IN_REVIEW, WorkflowStatus.COMPLETED],
                            std_index + req_index,
                            WorkflowStatus.PLANNED,
                        ),
                        "conformity_level": self.pick(
                            [ConformityLevel.PARTIAL, ConformityLevel.NON_CONFORMANT, ConformityLevel.CONFORMANT],
                            std_index + req_index,
                            ConformityLevel.PARTIAL,
                        ),
                        "assessed_on": self.today - timedelta(days=std_index * req_index + 3),
                        "next_review_date": self.today + timedelta(days=25 + std_index * req_index),
                        "assessor_name": self.pick(self.users, std_index + req_index).get_full_name()
                        if self.users
                        else "Compliance Assessor",
                        "score": 58 + std_index * 7 + req_index * 3,
                        "evidence_summary": "Configuration extracts, governance approvals, and operating logs reviewed.",
                        "gap_summary": "Control maturity varies across institutions; escalation and documentation need reinforcement.",
                        "recommendation_summary": "Close documentation gaps and align operational rehearsal cadence.",
                        "follow_up_action": "Raise corrective action and link remediation owner.",
                        "notes": "Generated by seed_extended_operational_demo.",
                    },
                )[0]
                assessments.append(assessment)

                self.upsert(
                    ControlEvidence,
                    {
                        "organization": self.organization,
                        "title": f"{assessment.title} - evidence pack",
                    },
                    {
                        "related_assessment": assessment,
                        "related_standard": standard,
                        "related_requirement": requirement,
                        "related_control": control,
                        "evidence_type": self.pick(
                            [EvidenceType.DOCUMENT, EvidenceType.CONFIGURATION, EvidenceType.LOG, EvidenceType.REPORT],
                            req_index,
                            EvidenceType.DOCUMENT,
                        ),
                        "status": self.pick(
                            [EvidenceStatus.AVAILABLE, EvidenceStatus.REVIEWED, EvidenceStatus.PENDING],
                            req_index + std_index,
                            EvidenceStatus.AVAILABLE,
                        ),
                        "reference_url": f"https://docs.opengrc.local/compliance/{assessment.id}/evidence",
                        "reference_label": "Compliance evidence pack",
                        "captured_on": self.today - timedelta(days=req_index),
                        "validity_until": self.today + timedelta(days=90),
                        "owner_name": assessment.assessor_name,
                        "notes": "Generated by seed_extended_operational_demo.",
                    },
                )

        for index, framework in enumerate(frameworks, start=1):
            audit_plan = self.upsert(
                AuditPlan,
                {
                    "organization": self.organization,
                    "title": f"{framework.title} - operational audit cycle {index}",
                },
                {
                    "related_framework": framework,
                    "related_standard": self.pick(standards, index - 1),
                    "target_stakeholder": self.pick(self.stakeholders, index + 10),
                    "related_infrastructure": self.pick(self.infrastructure, index + 2),
                    "scope": "Operational readiness, evidence completeness, and incident escalation preparedness.",
                    "status": self.pick(
                        [WorkflowStatus.PLANNED, WorkflowStatus.IN_PROGRESS, WorkflowStatus.IN_REVIEW],
                        index,
                        WorkflowStatus.PLANNED,
                    ),
                    "planned_start_date": self.today - timedelta(days=index * 5),
                    "planned_end_date": self.today + timedelta(days=index * 7),
                    "actual_end_date": None if index < 3 else self.today - timedelta(days=1),
                    "lead_auditor": self.pick(self.users, index).get_full_name() if self.users else "Lead Auditor",
                    "objectives": "Test operational control execution and governance evidence quality.",
                    "sampling_strategy": "Sample one institution, one operator, and one critical asset per sector.",
                    "summary": "Seeded audit plan for report and workflow testing.",
                    "next_step": "Complete checklist walkthrough and validate findings.",
                    "notes": "Generated by seed_extended_operational_demo.",
                },
            )[0]
            audit_plans.append(audit_plan)

            related_requirements = requirements[index - 1 : index + 2] or requirements[:3]
            for item_order, requirement in enumerate(related_requirements, start=1):
                control = StandardControl.objects.filter(related_requirement=requirement).first()
                checklist = self.upsert(
                    AuditChecklist,
                    {
                        "organization": self.organization,
                        "audit_plan": audit_plan,
                        "item_order": item_order,
                    },
                    {
                        "related_requirement": requirement,
                        "related_control": control,
                        "title": f"{audit_plan.title} - checklist item {item_order}",
                        "verification_procedure": "Interview operator focal points and inspect current evidence.",
                        "expected_evidence": "Signed approvals, technical logs, review records, and recent rehearsal outputs.",
                        "status": self.pick(
                            [ChecklistStatus.COMPLETED, ChecklistStatus.IN_PROGRESS, ChecklistStatus.BLOCKED],
                            index + item_order,
                            ChecklistStatus.PLANNED,
                        ),
                        "result": self.pick(
                            [ConformityLevel.CONFORMANT, ConformityLevel.PARTIAL, ConformityLevel.NON_CONFORMANT],
                            item_order,
                            ConformityLevel.PARTIAL,
                        ),
                        "finding_summary": "Evidence gaps identified where documentation and rehearsal trails are stale.",
                        "evidence_reference": f"https://docs.opengrc.local/audit/{audit_plan.id}/checklist/{item_order}",
                        "notes": "Generated by seed_extended_operational_demo.",
                    },
                )[0]

                if item_order < 3:
                    finding = self.upsert(
                        AuditFinding,
                        {
                            "organization": self.organization,
                            "audit_plan": audit_plan,
                            "title": f"{audit_plan.title} - finding {item_order}",
                        },
                        {
                            "checklist_item": checklist,
                            "related_assessment": self.pick(assessments, index + item_order),
                            "related_requirement": requirement,
                            "related_control": control,
                            "severity": self.pick(
                                [PriorityLevel.HIGH, PriorityLevel.MEDIUM, PriorityLevel.CRITICAL],
                                index + item_order,
                                PriorityLevel.HIGH,
                            ),
                            "status": self.pick(
                                [FindingStatus.VALIDATED, FindingStatus.REMEDIATING, FindingStatus.IDENTIFIED],
                                item_order,
                                FindingStatus.IDENTIFIED,
                            ),
                            "due_date": self.today + timedelta(days=20 + item_order * 4),
                            "owner_name": self.pick(self.stakeholders, index + item_order + 12).name,
                            "impact_summary": "Operational resilience would degrade if the gap remains unresolved.",
                            "recommendation": "Refresh evidence, confirm ownership, and run a targeted validation exercise.",
                            "evidence_reference": checklist.evidence_reference,
                            "notes": "Generated by seed_extended_operational_demo.",
                        },
                    )[0]
                    findings.append(finding)

                    non_conformity = self.upsert(
                        NonConformity,
                        {
                            "organization": self.organization,
                            "audit_finding": finding,
                            "title": f"{finding.title} - non-conformity",
                        },
                        {
                            "related_assessment": finding.related_assessment,
                            "related_requirement": finding.related_requirement,
                            "related_control": finding.related_control,
                            "severity": finding.severity,
                            "status": self.pick(
                                [NonConformityStatus.OPEN, NonConformityStatus.REMEDIATING, NonConformityStatus.IN_REVIEW],
                                item_order,
                                NonConformityStatus.OPEN,
                            ),
                            "due_date": finding.due_date,
                            "owner_name": finding.owner_name,
                            "root_cause": "Evidence and ownership refresh cycles were not synchronized across the institutions.",
                            "containment_action": "Record compensating controls and confirm interim approvals.",
                            "remediation_expectation": "Update evidence and complete management sign-off before the due date.",
                            "verification_notes": "Verification required during the next review cycle.",
                            "notes": "Generated by seed_extended_operational_demo.",
                        },
                    )[0]
                    non_conformities.append(non_conformity)

                    self.upsert(
                        CorrectiveAction,
                        {
                            "organization": self.organization,
                            "title": f"{finding.title} - corrective action",
                        },
                        {
                            "related_finding": finding,
                            "related_non_conformity": non_conformity,
                            "related_assessment": finding.related_assessment,
                            "related_control": finding.related_control,
                            "related_infrastructure": audit_plan.related_infrastructure,
                            "owner_name": finding.owner_name,
                            "priority": finding.severity,
                            "status": self.pick(
                                [WorkflowStatus.IN_PROGRESS, WorkflowStatus.PLANNED, WorkflowStatus.IN_REVIEW],
                                index + item_order,
                                WorkflowStatus.PLANNED,
                            ),
                            "start_date": self.today - timedelta(days=4),
                            "due_date": finding.due_date,
                            "completed_date": None,
                            "action_summary": "Refresh governance approvals, align evidence owners, and rehearse the control.",
                            "success_metric": "Updated evidence accepted and non-conformity status moved to resolved.",
                            "blocker_summary": "Awaiting one operator-side approval." if item_order == 2 else "",
                            "evidence_reference": finding.evidence_reference,
                            "verification_notes": "To be validated during the next audit cycle.",
                            "notes": "Generated by seed_extended_operational_demo.",
                        },
                    )

        return {
            "standards": standards,
            "requirements": requirements,
            "controls": controls,
            "assessments": assessments,
            "audit_plans": audit_plans,
            "findings": findings,
            "non_conformities": non_conformities,
        }

    def seed_intelligence(self):
        asset_items = []
        threat_events = []
        vulnerabilities = []
        risk_scenarios = []
        bulletins = []
        distribution_groups = []

        asset_specs = [
            ("National CERT ticketing platform", AssetInventoryType.PLATFORM, "Banjul"),
            ("Interbank switching service", AssetInventoryType.APPLICATION, "Banjul"),
            ("National fibre backbone segment A", AssetInventoryType.NETWORK, "Kanifing"),
            ("Gov identity database cluster", AssetInventoryType.DATA, "Brikama"),
            ("Emergency coordination room", AssetInventoryType.FACILITY, "Banjul"),
            ("National alerting roster team", AssetInventoryType.TEAM, "Kanifing"),
            ("Sector crisis communications process", AssetInventoryType.PROCESS, "Banjul"),
            ("Regional service desk", AssetInventoryType.SERVICE, "Farafenni"),
        ]
        latitudes = [Decimal("13.454876"), Decimal("13.443210"), Decimal("13.405500"), Decimal("13.476230")]
        longitudes = [Decimal("-16.579032"), Decimal("-16.673190"), Decimal("-16.694120"), Decimal("-16.577340")]

        for index, (name, asset_type, admin_area) in enumerate(asset_specs, start=1):
            infrastructure = self.pick(self.infrastructure, index)
            stakeholder = infrastructure.owner_stakeholder or self.pick(self.stakeholders, index)
            asset = self.upsert(
                AssetInventoryItem,
                {"organization": self.organization, "code": f"ASSET-INV-{index:03d}"},
                {
                    "owner_stakeholder": stakeholder,
                    "related_infrastructure": infrastructure,
                    "sector_ref": infrastructure.sector_ref,
                    "name": name,
                    "asset_type": asset_type,
                    "sector": infrastructure.sector,
                    "owner_name": stakeholder.name if stakeholder else infrastructure.owner_name,
                    "essential_function": f"Support {infrastructure.essential_service or infrastructure.name.lower()} continuity.",
                    "admin_area": admin_area,
                    "location": infrastructure.location or admin_area,
                    "latitude": latitudes[index % len(latitudes)],
                    "longitude": longitudes[index % len(longitudes)],
                    "criticality_level": self.pick(
                        [PriorityLevel.HIGH, PriorityLevel.CRITICAL, PriorityLevel.MEDIUM],
                        index,
                        PriorityLevel.HIGH,
                    ),
                    "dependency_summary": "Relies on telecom connectivity, identity services, and operator coordination.",
                    "summary": "Seeded asset inventory item for risk, threat, and map scenarios.",
                    "status": self.pick(
                        [WorkflowStatus.ACTIVE, WorkflowStatus.IN_REVIEW, WorkflowStatus.VALIDATED],
                        index,
                        WorkflowStatus.ACTIVE,
                    ),
                    "notes": "Generated by seed_extended_operational_demo.",
                },
            )[0]
            sync_point_geometry(asset)
            asset.save(update_fields=["geometry_geojson", "updated_at"])
            asset_items.append(asset)

            threat_event = self.upsert(
                ThreatEvent,
                {"organization": self.organization, "title": f"{name} - threat event"},
                {
                    "reporting_stakeholder": stakeholder,
                    "related_infrastructure": infrastructure,
                    "asset_item": asset,
                    "threat_type": self.pick(
                        [ThreatType.MALWARE, ThreatType.PHISHING, ThreatType.DDOS, ThreatType.RANSOMWARE, ThreatType.SUPPLY_CHAIN],
                        index,
                        ThreatType.OTHER,
                    ),
                    "threat_source_type": self.pick(
                        [ThreatSourceType.MONITORING, ThreatSourceType.CERT, ThreatSourceType.VENDOR, ThreatSourceType.PARTNER],
                        index,
                        ThreatSourceType.MONITORING,
                    ),
                    "status": self.pick(
                        [ThreatEventStatus.ANALYZING, ThreatEventStatus.MONITORED, ThreatEventStatus.MITIGATED],
                        index,
                        ThreatEventStatus.IDENTIFIED,
                    ),
                    "severity": self.pick(
                        [PriorityLevel.HIGH, PriorityLevel.CRITICAL, PriorityLevel.MEDIUM],
                        index + 1,
                        PriorityLevel.HIGH,
                    ),
                    "confidence_level": self.pick(
                        [PriorityLevel.MEDIUM, PriorityLevel.HIGH],
                        index,
                        PriorityLevel.MEDIUM,
                    ),
                    "first_seen_at": self.now - timedelta(days=index, hours=4),
                    "last_seen_at": self.now - timedelta(hours=index),
                    "admin_area": admin_area,
                    "location": asset.location,
                    "latitude": asset.latitude,
                    "longitude": asset.longitude,
                    "suspected_actor": self.pick(
                        ["Commodity ransomware cluster", "State-linked operator", "Fraud syndicate", "Disruption campaign"],
                        index,
                        "Threat actor",
                    ),
                    "summary": "Multi-source reporting indicates elevated cyber activity around this asset.",
                    "recommended_action": "Raise sector alerting posture and validate operator readiness.",
                    "notes": "Generated by seed_extended_operational_demo.",
                },
            )[0]
            sync_point_geometry(threat_event)
            threat_event.save(update_fields=["geometry_geojson", "updated_at"])
            threat_events.append(threat_event)

            vulnerability = self.upsert(
                VulnerabilityRecord,
                {"organization": self.organization, "title": f"{name} - vulnerability"},
                {
                    "related_infrastructure": infrastructure,
                    "asset_item": asset,
                    "related_threat_event": threat_event,
                    "vulnerability_type": self.pick(
                        ["Identity misconfiguration", "Patch backlog", "Weak filtering", "Insecure remote access"],
                        index,
                        "Operational weakness",
                    ),
                    "severity": self.pick(
                        [PriorityLevel.HIGH, PriorityLevel.CRITICAL, PriorityLevel.MEDIUM],
                        index,
                        PriorityLevel.HIGH,
                    ),
                    "status": self.pick(
                        [VulnerabilityStatus.REMEDIATING, VulnerabilityStatus.VALIDATING, VulnerabilityStatus.IDENTIFIED],
                        index,
                        VulnerabilityStatus.IDENTIFIED,
                    ),
                    "exploitability_level": self.pick(
                        [PriorityLevel.HIGH, PriorityLevel.MEDIUM, PriorityLevel.CRITICAL],
                        index + 2,
                        PriorityLevel.HIGH,
                    ),
                    "discovered_on": self.today - timedelta(days=index + 5),
                    "remediation_due_date": self.today + timedelta(days=20 + index),
                    "owner_name": stakeholder.name if stakeholder else "Infrastructure owner",
                    "summary": "Observed weakness could widen service disruption if threat activity intensifies.",
                    "remediation_guidance": "Apply compensating controls, confirm ownership, and verify closure evidence.",
                    "notes": "Generated by seed_extended_operational_demo.",
                },
            )[0]
            vulnerabilities.append(vulnerability)

            risk_scenario = self.upsert(
                RiskScenario,
                {"organization": self.organization, "title": f"{name} - risk scenario"},
                {
                    "risk_register_entry": self.pick(self.risks, index),
                    "related_infrastructure": infrastructure,
                    "asset_item": asset,
                    "related_threat_event": threat_event,
                    "vulnerability_record": vulnerability,
                    "status": self.pick(
                        [WorkflowStatus.IN_PROGRESS, WorkflowStatus.IN_REVIEW, WorkflowStatus.VALIDATED],
                        index,
                        WorkflowStatus.DRAFT,
                    ),
                    "risk_level": self.pick(
                        [PriorityLevel.HIGH, PriorityLevel.CRITICAL, PriorityLevel.MEDIUM],
                        index + 3,
                        PriorityLevel.HIGH,
                    ),
                    "treatment_status": self.pick(
                        [RiskTreatmentStatus.MITIGATING, RiskTreatmentStatus.ASSESSING, RiskTreatmentStatus.IDENTIFIED],
                        index,
                        RiskTreatmentStatus.IDENTIFIED,
                    ),
                    "scenario_owner": stakeholder.name if stakeholder else "Scenario owner",
                    "likelihood": 3 + (index % 2),
                    "impact": 4 + (index % 2),
                    "risk_score": Decimal(str((3 + (index % 2)) * (4 + (index % 2)))),
                    "scenario_summary": "Compromise of this asset could disrupt national service delivery and coordination workflows.",
                    "business_impact": "Elevated service interruption, reputational impact, and cross-sector coordination pressure.",
                    "response_plan": "Escalate to national coordination, activate the linked contingency plan, and allocate response assets.",
                    "review_due_date": self.today + timedelta(days=15 + index),
                    "notes": "Generated by seed_extended_operational_demo.",
                },
            )[0]
            risk_scenarios.append(risk_scenario)

            self.upsert(
                RiskAssessmentReview,
                {"organization": self.organization, "title": f"{name} - risk review"},
                {
                    "risk_scenario": risk_scenario,
                    "risk_register_entry": risk_scenario.risk_register_entry,
                    "reviewer_stakeholder": self.pick(self.stakeholders, index + 14),
                    "review_date": self.today - timedelta(days=index),
                    "decision": self.pick(
                        [RiskReviewDecision.MITIGATE, RiskReviewDecision.MONITOR, RiskReviewDecision.ESCALATE],
                        index,
                        RiskReviewDecision.MONITOR,
                    ),
                    "status": self.pick(
                        [WorkflowStatus.COMPLETED, WorkflowStatus.IN_REVIEW, WorkflowStatus.PLANNED],
                        index,
                        WorkflowStatus.PLANNED,
                    ),
                    "residual_risk_level": self.pick(
                        [PriorityLevel.MEDIUM, PriorityLevel.HIGH],
                        index,
                        PriorityLevel.MEDIUM,
                    ),
                    "summary": "Risk reviewed against current operating posture and sector dependencies.",
                    "recommendations": "Prioritize mitigation ownership and validate contingency readiness before the next review.",
                    "follow_up_date": self.today + timedelta(days=10 + index),
                    "notes": "Generated by seed_extended_operational_demo.",
                },
            )

            bulletin = self.upsert(
                ThreatBulletin,
                {"organization": self.organization, "title": f"{name} - threat bulletin"},
                {
                    "related_threat_event": threat_event,
                    "related_infrastructure": infrastructure,
                    "target_sector_ref": infrastructure.sector_ref,
                    "bulletin_type": self.pick(
                        [BulletinType.ALERT, BulletinType.ADVISORY, BulletinType.COORDINATION],
                        index,
                        BulletinType.ADVISORY,
                    ),
                    "severity": threat_event.severity,
                    "status": self.pick(
                        [WorkflowStatus.VALIDATED, WorkflowStatus.IN_REVIEW, WorkflowStatus.ACTIVE],
                        index,
                        WorkflowStatus.DRAFT,
                    ),
                    "issued_on": self.today - timedelta(days=index),
                    "valid_until": self.today + timedelta(days=7 + index),
                    "target_sector": infrastructure.sector,
                    "summary": "Sector partners should tighten monitoring and confirm readiness status.",
                    "recommended_actions": "Inspect indicators, refresh access reviews, and report abnormal activity through the platform.",
                    "source_reference": f"https://intel.opengrc.local/bulletins/{index}",
                    "notes": "Generated by seed_extended_operational_demo.",
                },
            )[0]
            bulletins.append(bulletin)

            self.upsert(
                Indicator,
                {"organization": self.organization, "title": f"{name} - primary indicator"},
                {
                    "related_bulletin": bulletin,
                    "related_threat_event": threat_event,
                    "indicator_type": self.pick(
                        [IndicatorType.IP, IndicatorType.DOMAIN, IndicatorType.URL, IndicatorType.EMAIL],
                        index,
                        IndicatorType.IP,
                    ),
                    "value": self.pick(
                        [
                            f"196.46.232.{20 + index}",
                            f"alert-{index}.national-gm.example",
                            f"https://alerts.example/{index}",
                            f"notify{index}@example-threat.io",
                        ],
                        index,
                        f"indicator-{index}",
                    ),
                    "status": self.pick(
                        [IndicatorStatus.ACTIVE, IndicatorStatus.MONITORING, IndicatorStatus.NEW],
                        index,
                        IndicatorStatus.NEW,
                    ),
                    "confidence_level": threat_event.confidence_level,
                    "first_seen_at": threat_event.first_seen_at,
                    "last_seen_at": threat_event.last_seen_at,
                    "notes": "Generated by seed_extended_operational_demo.",
                },
            )

        group_specs = [
            ("Energy sector operations group", DistributionGroupType.SECTOR, 0, [0, 1, 2]),
            ("Telecom coordination group", DistributionGroupType.SECTOR, 1, [3, 4, 5]),
            ("Financial services continuity group", DistributionGroupType.SECTOR, 2, [6, 7, 8]),
            ("National cyber coordination group", DistributionGroupType.NATIONAL, 0, [0, 4, 8, 12]),
        ]
        for title, group_type, sector_index, stakeholder_indices in group_specs:
            group = self.upsert(
                DistributionGroup,
                {"organization": self.organization, "title": title},
                {
                    "group_type": group_type,
                    "target_sector_ref": self.pick(self.sectors, sector_index),
                    "target_sector": self.pick(self.sectors, sector_index).name if self.sectors else "",
                    "status": WorkflowStatus.ACTIVE,
                    "distribution_notes": "Seeded national information-sharing group.",
                },
            )[0]
            group.stakeholders.set([self.pick(self.stakeholders, idx) for idx in stakeholder_indices if self.stakeholders])
            distribution_groups.append(group)

        for index, bulletin in enumerate(bulletins[:6], start=1):
            group = self.pick(distribution_groups, index)
            target_stakeholder = self.pick(self.stakeholders, index + 20)
            share = self.upsert(
                InformationShare,
                {"organization": self.organization, "title": f"{bulletin.title} - distribution"},
                {
                    "related_bulletin": bulletin,
                    "related_threat_event": bulletin.related_threat_event,
                    "distribution_group": group,
                    "target_stakeholder": target_stakeholder,
                    "share_channel": self.pick(
                        [ShareChannel.PLATFORM, ShareChannel.EMAIL, ShareChannel.BRIEFING, ShareChannel.MEETING],
                        index,
                        ShareChannel.PLATFORM,
                    ),
                    "status": self.pick(
                        [ShareStatus.SHARED, ShareStatus.ACKNOWLEDGED, ShareStatus.PREPARED],
                        index,
                        ShareStatus.SHARED,
                    ),
                    "shared_at": self.now - timedelta(hours=index * 3),
                    "acknowledgement_due_date": self.today + timedelta(days=index),
                    "action_requested": "Confirm exposure status and return any sector-level operational constraints.",
                    "access_link": f"https://platform.opengrc.local/shares/{index}",
                    "message_summary": "Bulletin shared with targeted institutions and sector groups.",
                    "notes": "Generated by seed_extended_operational_demo.",
                },
            )[0]

            self.upsert(
                Acknowledgement,
                {
                    "organization": self.organization,
                    "information_share": share,
                    "stakeholder": target_stakeholder,
                },
                {
                    "status": self.pick(
                        [AcknowledgementStatus.RECEIVED, AcknowledgementStatus.ACTIONED, AcknowledgementStatus.PENDING],
                        index,
                        AcknowledgementStatus.PENDING,
                    ),
                    "responded_at": self.now - timedelta(hours=index) if index < 5 else None,
                    "action_note": "Sector focal point confirmed receipt and launched local validation.",
                    "notes": "Generated by seed_extended_operational_demo.",
                },
            )

        return {
            "asset_items": asset_items,
            "threat_events": threat_events,
            "vulnerabilities": vulnerabilities,
            "risk_scenarios": risk_scenarios,
            "bulletins": bulletins,
            "distribution_groups": distribution_groups,
        }

    def seed_documents_and_reviews(self, *, incident_context, compliance_context, intelligence_context):
        document_specs = [
            {
                "title": "National incident operations situation report",
                "module_key": "incidents",
                "module_label": "Incident Operations",
                "document_type": DocumentType.REPORT,
                "output_format": "pdf",
                "rows": [
                    {
                        "title": incident.title,
                        "severity": incident.severity,
                        "status": incident.status,
                        "lead_stakeholder": incident.lead_stakeholder.name if incident.lead_stakeholder else "",
                        "reported_at": incident.reported_at,
                        "next_update_due": incident.next_update_due,
                        "summary": incident.summary,
                    }
                    for incident in incident_context["incidents"]
                ],
                "record_title": "National incident operations snapshot",
            },
            {
                "title": "Threat intelligence dissemination pack",
                "module_key": "threat_bulletins",
                "module_label": "Threat Bulletins",
                "document_type": DocumentType.BRIEF,
                "output_format": "docx",
                "rows": [
                    {
                        "title": bulletin.title,
                        "bulletin_type": bulletin.bulletin_type,
                        "severity": bulletin.severity,
                        "target_sector": bulletin.target_sector,
                        "issued_on": bulletin.issued_on,
                        "valid_until": bulletin.valid_until,
                        "recommended_actions": bulletin.recommended_actions,
                    }
                    for bulletin in intelligence_context["bulletins"][:6]
                ],
                "record_title": "Threat dissemination package",
            },
            {
                "title": "Compliance and audit readiness dossier",
                "module_key": "audit_findings",
                "module_label": "Audit Findings",
                "document_type": DocumentType.DOSSIER,
                "output_format": "pdf",
                "rows": [
                    {
                        "title": finding.title,
                        "severity": finding.severity,
                        "status": finding.status,
                        "owner_name": finding.owner_name,
                        "due_date": finding.due_date,
                        "recommendation": finding.recommendation,
                    }
                    for finding in compliance_context["findings"][:8]
                ],
                "record_title": "Compliance readiness dossier",
            },
            {
                "title": "National cyber risk scenario brief",
                "module_key": "risk_scenarios",
                "module_label": "Risk Scenarios",
                "document_type": DocumentType.BRIEF,
                "output_format": "docx",
                "rows": [
                    {
                        "title": scenario.title,
                        "risk_level": scenario.risk_level,
                        "treatment_status": scenario.treatment_status,
                        "scenario_owner": scenario.scenario_owner,
                        "review_due_date": scenario.review_due_date,
                        "business_impact": scenario.business_impact,
                    }
                    for scenario in intelligence_context["risk_scenarios"][:8]
                ],
                "record_title": "Risk scenario portfolio",
            },
        ]

        for index, spec in enumerate(document_specs, start=1):
            document = self.build_document_record(
                title=spec["title"],
                module_key=spec["module_key"],
                module_label=spec["module_label"],
                document_type=spec["document_type"],
                output_format=spec["output_format"],
                rows=spec["rows"],
                record_title=spec["record_title"],
            )

            review_cycle = self.upsert(
                ReviewCycle,
                {"organization": self.organization, "title": f"{spec['title']} review cycle"},
                {
                    "generated_document": document,
                    "module_key": spec["module_key"],
                    "module_label": spec["module_label"],
                    "record_id": document.record_id,
                    "record_title": spec["record_title"],
                    "owner_name": self.pick(self.stakeholders, index + 30).name,
                    "cadence_days": 30 + index * 15,
                    "status": self.pick(
                        [ReviewCycleStatus.ACTIVE, ReviewCycleStatus.OVERDUE, ReviewCycleStatus.COMPLETED],
                        index,
                        ReviewCycleStatus.ACTIVE,
                    ),
                    "current_version_label": document.version_label,
                    "last_review_date": self.today - timedelta(days=7 + index),
                    "next_review_date": self.today + timedelta(days=21 + index * 3),
                    "scope_summary": f"Recurring review cycle for {spec['module_label'].lower()} outputs.",
                    "notes": "Generated by seed_extended_operational_demo.",
                },
            )[0]

            review_record = self.upsert(
                ReviewRecord,
                {
                    "organization": self.organization,
                    "title": f"{spec['title']} review record",
                },
                {
                    "review_cycle": review_cycle,
                    "generated_document": document,
                    "review_date": self.today - timedelta(days=5 + index),
                    "decision": self.pick(
                        [ReviewDecision.APPROVED, ReviewDecision.CHANGES_REQUESTED, ReviewDecision.SUPERSEDED],
                        index,
                        ReviewDecision.APPROVED,
                    ),
                    "status": WorkflowStatus.COMPLETED,
                    "reviewer_name": self.pick(self.users, index).get_full_name() if self.users else "Review Board",
                    "summary": "Review completed against operational quality and ToR traceability expectations.",
                    "recommendations": "Maintain evidence freshness and confirm the next review milestone.",
                    "next_review_date": review_cycle.next_review_date,
                    "version_label": document.version_label,
                    "notes": "Generated by seed_extended_operational_demo.",
                },
            )[0]

            log_specs = [
                ("Document generated", ChangeType.GENERATED),
                ("Review cycle started", ChangeType.REVIEW_STARTED),
                ("Review decision recorded", ChangeType.REVIEW_RECORDED),
            ]
            if review_record.decision == ReviewDecision.APPROVED:
                log_specs.append(("Document approved", ChangeType.APPROVED))
            elif review_record.decision == ReviewDecision.SUPERSEDED:
                log_specs.append(("Document superseded", ChangeType.SUPERSEDED))
            else:
                log_specs.append(("Document updated", ChangeType.UPDATED))

            for log_index, (log_title, change_type) in enumerate(log_specs, start=1):
                self.upsert(
                    ChangeLogEntry,
                    {
                        "organization": self.organization,
                        "title": f"{spec['title']} - {log_title}",
                    },
                    {
                        "generated_document": document,
                        "review_cycle": review_cycle,
                        "review_record": review_record,
                        "module_key": spec["module_key"],
                        "module_label": spec["module_label"],
                        "record_id": document.record_id,
                        "record_title": spec["record_title"],
                        "change_type": change_type,
                        "version_label": document.version_label,
                        "summary": f"{log_title} for {spec['title'].lower()}.",
                        "change_metadata": {
                            "document_type": document.document_type,
                            "output_format": document.output_format,
                            "decision": review_record.decision,
                        },
                        "changed_on": self.now - timedelta(days=index, hours=log_index),
                        "changed_by_name": self.pick(self.stakeholders, index + 35).name,
                    },
                )
