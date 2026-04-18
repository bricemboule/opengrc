from django.conf import settings
from django.db import models

from apps.core.models import SoftDeleteAuditModel


class IncidentType(models.TextChoices):
    SERVICE_OUTAGE = "service_outage", "Service outage"
    MALWARE = "malware", "Malware"
    DATA_BREACH = "data_breach", "Data breach"
    PHISHING = "phishing", "Phishing"
    DDOS = "ddos", "DDoS"
    UNAUTHORIZED_ACCESS = "unauthorized_access", "Unauthorized access"
    FRAUD = "fraud", "Fraud"
    PHYSICAL_INTRUSION = "physical_intrusion", "Physical intrusion"
    SUPPLY_CHAIN = "supply_chain", "Supply chain"
    OTHER = "other", "Other"


class IncidentSeverity(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    CRITICAL = "critical", "Critical"
    NATIONAL = "national", "National significance"


class IncidentStatus(models.TextChoices):
    REPORTED = "reported", "Reported"
    ASSESSING = "assessing", "Assessing"
    ACTIVE = "active", "Active"
    CONTAINED = "contained", "Contained"
    RECOVERING = "recovering", "Recovering"
    CLOSED = "closed", "Closed"


class IncidentSource(models.TextChoices):
    INTERNAL_REPORT = "internal_report", "Internal report"
    EXTERNAL_REPORT = "external_report", "External report"
    MONITORING = "monitoring", "Monitoring alert"
    THREAT_INTELLIGENCE = "threat_intelligence", "Threat intelligence"
    EXERCISE = "exercise", "Exercise"
    CONSULTATION = "consultation", "Consultation"
    OTHER = "other", "Other"


class IncidentUpdateType(models.TextChoices):
    SITUATION = "situation", "Situation update"
    DECISION = "decision", "Decision"
    ESCALATION = "escalation", "Escalation"
    CONTAINMENT = "containment", "Containment"
    RECOVERY = "recovery", "Recovery"
    LESSON = "lesson", "Lesson learned"


class IncidentTaskStatus(models.TextChoices):
    PLANNED = "planned", "Planned"
    IN_PROGRESS = "in_progress", "In progress"
    BLOCKED = "blocked", "Blocked"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class IncidentAssignmentStatus(models.TextChoices):
    ASSIGNED = "assigned", "Assigned"
    ACKNOWLEDGED = "acknowledged", "Acknowledged"
    ACTIVE = "active", "Active"
    RELEASED = "released", "Released"


class CommunicationDirection(models.TextChoices):
    OUTBOUND = "outbound", "Outbound"
    INBOUND = "inbound", "Inbound"


class CommunicationChannel(models.TextChoices):
    EMAIL = "email", "Email"
    PHONE = "phone", "Phone"
    VIDEO = "video", "Video"
    SMS = "sms", "SMS"
    BRIEFING = "briefing", "Briefing"
    BULLETIN = "bulletin", "Bulletin"
    OTHER = "other", "Other"


class AttachmentType(models.TextChoices):
    LOG = "log", "Log"
    REPORT = "report", "Report"
    SCREENSHOT = "screenshot", "Screenshot"
    EVIDENCE = "evidence", "Evidence"
    BULLETIN = "bulletin", "Bulletin"
    OTHER = "other", "Other"


class SOPTemplateStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    READY = "ready", "Ready"
    ACTIVE = "active", "Active"
    ARCHIVED = "archived", "Archived"


class SOPStepType(models.TextChoices):
    CHECK = "check", "Checklist"
    DECISION = "decision", "Decision"
    COMMUNICATION = "communication", "Communication"
    ESCALATION = "escalation", "Escalation"
    TECHNICAL = "technical", "Technical"
    EVIDENCE = "evidence", "Evidence capture"


class SOPExecutionStatus(models.TextChoices):
    PLANNED = "planned", "Planned"
    ACTIVE = "active", "Active"
    BLOCKED = "blocked", "Blocked"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class SOPExecutionStepStatus(models.TextChoices):
    PLANNED = "planned", "Planned"
    IN_PROGRESS = "in_progress", "In progress"
    BLOCKED = "blocked", "Blocked"
    COMPLETED = "completed", "Completed"
    SKIPPED = "skipped", "Skipped"


class AllocationStatus(models.TextChoices):
    REQUESTED = "requested", "Requested"
    APPROVED = "approved", "Approved"
    MOBILIZING = "mobilizing", "Mobilizing"
    DEPLOYED = "deployed", "Deployed"
    DEMOBILIZING = "demobilizing", "Demobilizing"
    RELEASED = "released", "Released"
    CANCELLED = "cancelled", "Cancelled"


class Incident(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="incidents")
    title = models.CharField(max_length=255)
    incident_type = models.CharField(max_length=40, choices=IncidentType.choices, default=IncidentType.SERVICE_OUTAGE)
    severity = models.CharField(max_length=24, choices=IncidentSeverity.choices, default=IncidentSeverity.MEDIUM)
    status = models.CharField(max_length=24, choices=IncidentStatus.choices, default=IncidentStatus.REPORTED)
    source = models.CharField(max_length=40, choices=IncidentSource.choices, default=IncidentSource.INTERNAL_REPORT)
    detected_at = models.DateTimeField(null=True, blank=True)
    reported_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    summary = models.TextField(blank=True)
    operational_objective = models.TextField(blank=True)
    cross_sector_impact = models.TextField(blank=True)
    decision_log = models.TextField(blank=True)
    lessons_learned = models.TextField(blank=True)
    external_reference = models.CharField(max_length=120, blank=True)
    next_update_due = models.DateTimeField(null=True, blank=True)
    containment_target_at = models.DateTimeField(null=True, blank=True)
    recovery_target_at = models.DateTimeField(null=True, blank=True)
    national_significance = models.BooleanField(default=False)
    incident_coordinator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="coordinated_incidents",
    )
    lead_stakeholder = models.ForeignKey(
        "cybergrc.Stakeholder",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incidents",
    )
    linked_plan = models.ForeignKey(
        "cybergrc.ContingencyPlan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incidents",
    )
    affected_sectors = models.ManyToManyField("cybergrc.Sector", blank=True, related_name="incidents")
    affected_infrastructure = models.ManyToManyField("cybergrc.CriticalInfrastructure", blank=True, related_name="incidents")

    class Meta:
        ordering = ["-reported_at", "-created_at", "-id"]

    def __str__(self):
        return self.title


class IncidentUpdate(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="incident_updates")
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="updates")
    title = models.CharField(max_length=255)
    update_type = models.CharField(max_length=32, choices=IncidentUpdateType.choices, default=IncidentUpdateType.SITUATION)
    message = models.TextField()
    status_snapshot = models.CharField(max_length=24, choices=IncidentStatus.choices, blank=True)
    severity_snapshot = models.CharField(max_length=24, choices=IncidentSeverity.choices, blank=True)
    recorded_at = models.DateTimeField()
    next_step = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-recorded_at", "-id"]

    def __str__(self):
        return self.title


class IncidentTask(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="incident_tasks")
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=24, choices=IncidentTaskStatus.choices, default=IncidentTaskStatus.PLANNED)
    priority = models.CharField(max_length=24, choices=IncidentSeverity.choices, default=IncidentSeverity.MEDIUM)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incident_tasks",
    )
    due_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    blocker_summary = models.CharField(max_length=255, blank=True)
    next_step = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["completed_at", "due_at", "-created_at", "-id"]

    def __str__(self):
        return self.title


class IncidentAssignment(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="incident_assignments")
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="assignments")
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incident_assignments",
    )
    stakeholder = models.ForeignKey(
        "cybergrc.Stakeholder",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incident_assignments",
    )
    role_in_response = models.CharField(max_length=255)
    status = models.CharField(max_length=24, choices=IncidentAssignmentStatus.choices, default=IncidentAssignmentStatus.ASSIGNED)
    assigned_at = models.DateTimeField()
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    released_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-assigned_at", "-id"]

    def __str__(self):
        return f"{self.incident} - {self.role_in_response}"


class IncidentCommunication(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="incident_communications")
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="communications")
    subject = models.CharField(max_length=255)
    direction = models.CharField(max_length=24, choices=CommunicationDirection.choices, default=CommunicationDirection.OUTBOUND)
    channel = models.CharField(max_length=24, choices=CommunicationChannel.choices, default=CommunicationChannel.EMAIL)
    audience = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    sent_at = models.DateTimeField()
    external_reference = models.CharField(max_length=120, blank=True)
    requires_acknowledgement = models.BooleanField(default=False)

    class Meta:
        ordering = ["-sent_at", "-id"]

    def __str__(self):
        return self.subject


class IncidentAttachment(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="incident_attachments")
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="attachments")
    title = models.CharField(max_length=255)
    attachment_type = models.CharField(max_length=24, choices=AttachmentType.choices, default=AttachmentType.EVIDENCE)
    reference_url = models.URLField(blank=True)
    reference_label = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return self.title


class SOPTemplate(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="incident_sop_templates")
    contingency_plan = models.ForeignKey(
        "cybergrc.ContingencyPlan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incident_sop_templates",
    )
    related_artifact = models.ForeignKey(
        "cybergrc.GovernanceArtifact",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incident_sop_templates",
    )
    related_infrastructure = models.ForeignKey(
        "cybergrc.CriticalInfrastructure",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incident_sop_templates",
    )
    owner_stakeholder = models.ForeignKey(
        "cybergrc.Stakeholder",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incident_sop_templates",
    )
    code = models.CharField(max_length=80)
    title = models.CharField(max_length=255)
    version = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=24, choices=SOPTemplateStatus.choices, default=SOPTemplateStatus.DRAFT)
    objective = models.TextField(blank=True)
    activation_trigger = models.TextField(blank=True)
    review_notes = models.TextField(blank=True)
    last_reviewed_at = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["title", "-id"]
        constraints = [
            models.UniqueConstraint(fields=["organization", "code"], name="incident_sop_template_org_code_unique"),
        ]

    def __str__(self):
        return self.title


class SOPStep(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="incident_sop_steps")
    template = models.ForeignKey(SOPTemplate, on_delete=models.CASCADE, related_name="steps")
    step_order = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=255)
    instruction = models.TextField(blank=True)
    step_type = models.CharField(max_length=24, choices=SOPStepType.choices, default=SOPStepType.CHECK)
    is_required = models.BooleanField(default=True)
    responsible_role = models.CharField(max_length=255, blank=True)
    default_assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incident_sop_step_defaults",
    )
    estimated_duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    evidence_hint = models.CharField(max_length=255, blank=True)
    escalation_hint = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["step_order", "id"]
        constraints = [
            models.UniqueConstraint(fields=["template", "step_order"], name="incident_sop_step_template_order_unique"),
        ]

    def __str__(self):
        return f"{self.template.title} - Step {self.step_order}"


class SOPExecution(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="incident_sop_executions")
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="sop_executions")
    template = models.ForeignKey(SOPTemplate, on_delete=models.CASCADE, related_name="executions")
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=24, choices=SOPExecutionStatus.choices, default=SOPExecutionStatus.PLANNED)
    execution_commander = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incident_sop_executions",
    )
    started_at = models.DateTimeField(null=True, blank=True)
    target_completion_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    summary = models.TextField(blank=True)
    outcome_summary = models.TextField(blank=True)
    blocker_summary = models.TextField(blank=True)
    next_action = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-started_at", "-created_at", "-id"]

    def __str__(self):
        return self.title


class SOPExecutionStep(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="incident_sop_execution_steps")
    execution = models.ForeignKey(SOPExecution, on_delete=models.CASCADE, related_name="steps")
    template_step = models.ForeignKey(
        SOPStep,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="execution_steps",
    )
    step_order = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=255)
    instruction = models.TextField(blank=True)
    step_type = models.CharField(max_length=24, choices=SOPStepType.choices, default=SOPStepType.CHECK)
    status = models.CharField(max_length=24, choices=SOPExecutionStepStatus.choices, default=SOPExecutionStepStatus.PLANNED)
    is_required = models.BooleanField(default=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incident_sop_execution_steps",
    )
    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="completed_incident_sop_execution_steps",
    )
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    actual_duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    evidence_reference = models.URLField(blank=True)
    blocker_summary = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["step_order", "id"]
        constraints = [
            models.UniqueConstraint(fields=["execution", "step_order"], name="incident_sop_execution_step_order_unique"),
        ]

    def __str__(self):
        return f"{self.execution.title} - Step {self.step_order}"


class AssetAllocation(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="incident_asset_allocations")
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="asset_allocations")
    emergency_asset = models.ForeignKey(
        "cybergrc.EmergencyResponseAsset",
        on_delete=models.CASCADE,
        related_name="asset_allocations",
    )
    destination_infrastructure = models.ForeignKey(
        "cybergrc.CriticalInfrastructure",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="asset_allocations",
    )
    related_task = models.ForeignKey(
        IncidentTask,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="asset_allocations",
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_incident_asset_allocations",
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="requested_incident_asset_allocations",
    )
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=24, choices=AllocationStatus.choices, default=AllocationStatus.REQUESTED)
    priority = models.CharField(max_length=24, choices=IncidentSeverity.choices, default=IncidentSeverity.MEDIUM)
    quantity_requested = models.PositiveIntegerField(default=1)
    quantity_allocated = models.PositiveIntegerField(null=True, blank=True)
    requested_at = models.DateTimeField()
    approved_at = models.DateTimeField(null=True, blank=True)
    mobilized_at = models.DateTimeField(null=True, blank=True)
    deployed_at = models.DateTimeField(null=True, blank=True)
    released_at = models.DateTimeField(null=True, blank=True)
    destination = models.CharField(max_length=255, blank=True)
    deployment_notes = models.TextField(blank=True)
    release_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-requested_at", "-id"]

    def __str__(self):
        return self.title

