from django.db import models

from apps.core.models import SoftDeleteAuditModel


class WorkflowStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PLANNED = "planned", "Planned"
    IN_PROGRESS = "in_progress", "In progress"
    ACTIVE = "active", "Active"
    IN_REVIEW = "in_review", "In review"
    SUBMITTED = "submitted", "Submitted"
    VALIDATED = "validated", "Validated"
    COMPLETED = "completed", "Completed"
    ARCHIVED = "archived", "Archived"


class Phase(models.TextChoices):
    GOVERNANCE = "governance", "Governance framework"
    RISK = "risk", "Risk register"
    CONTINGENCY = "contingency", "Cyber contingency"
    STANDARDS = "standards", "Minimum standards"
    AUDIT = "audit", "Audit and protection"


class StakeholderType(models.TextChoices):
    GOVERNMENT = "government", "Government"
    REGULATOR = "regulator", "Regulator"
    OPERATOR = "operator", "Operator"
    BANK = "bank", "Bank"
    CII_OWNER = "cii_owner", "CII owner"
    CNI_OPERATOR = "cni_operator", "CNI operator"
    CERT = "cert", "CERT / CSIRT"
    PARTNER = "partner", "Partner"
    OTHER = "other", "Other"


class InfrastructureType(models.TextChoices):
    CII = "cii", "Critical information infrastructure"
    CNI = "cni", "Critical national infrastructure"


class DesignationStatus(models.TextChoices):
    IDENTIFIED = "identified", "Identified"
    DESIGNATED = "designated", "Designated"
    VALIDATED = "validated", "Validated"
    MONITORED = "monitored", "Monitored"


class MappingStatus(models.TextChoices):
    PLANNED = "planned", "Planned"
    IN_PROGRESS = "in_progress", "In progress"
    MAPPED = "mapped", "Mapped"
    REVIEWED = "reviewed", "Reviewed"


class AssuranceStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ASSESSING = "assessing", "Assessing"
    MITIGATING = "mitigating", "Mitigating"
    COMPLETED = "completed", "Completed"


class PriorityLevel(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    CRITICAL = "critical", "Critical"


class ArtifactType(models.TextChoices):
    POLICY = "policy", "Policy"
    REGULATION = "regulation", "Regulation"
    GUIDELINE = "guideline", "Guideline"
    FRAMEWORK = "framework", "Framework"
    SOP = "sop", "SOP"
    TEMPLATE = "template", "Template"
    REPORT = "report", "Report"
    SEP = "sep", "Stakeholder engagement plan"
    MAPPING_TOOL = "mapping_tool", "Mapping tool"
    GIS_MAP = "gis_map", "GIS map"
    ASSESSMENT = "assessment", "Assessment"
    ACTION_PLAN = "action_plan", "Action plan"


class DeskStudySourceType(models.TextChoices):
    POLICY = "policy", "Policy"
    REGULATION = "regulation", "Regulation"
    STANDARD = "standard", "Standard"
    INCIDENT = "incident", "Incident material"
    REPORT = "report", "Report"
    LEGAL = "legal", "Legal text"
    OTHER = "other", "Other"


class ConsultationType(models.TextChoices):
    BRIEFING = "briefing", "Briefing"
    INTERVIEW = "interview", "Interview"
    WORKSHOP = "workshop", "Workshop"
    VALIDATION = "validation", "Validation session"
    FIELD_VISIT = "field_visit", "Field visit"
    EXERCISE = "exercise", "Exercise coordination"


class EngagementChannel(models.TextChoices):
    IN_PERSON = "in_person", "In person"
    PHONE = "phone", "Phone"
    VIDEO = "video", "Video"
    HYBRID = "hybrid", "Hybrid"


class ConsultationStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SCHEDULED = "scheduled", "Scheduled"
    CONFIRMED = "confirmed", "Confirmed"
    COMPLETED = "completed", "Completed"
    MISSED = "missed", "Missed"
    RESCHEDULED = "rescheduled", "Rescheduled"
    ARCHIVED = "archived", "Archived"


class RiskTreatmentStatus(models.TextChoices):
    IDENTIFIED = "identified", "Identified"
    ASSESSING = "assessing", "Assessing"
    MITIGATING = "mitigating", "Mitigating"
    ACCEPTED = "accepted", "Accepted"
    CLOSED = "closed", "Closed"


class PlanType(models.TextChoices):
    NATIONAL = "national", "National"
    SECTORAL = "sectoral", "Sectoral"
    INCIDENT = "incident", "Incident response"
    RECOVERY = "recovery", "Recovery"
    COMMUNICATION = "communication", "Communication"


class EmergencyAssetType(models.TextChoices):
    DIGITAL = "digital", "Digital tool"
    PHYSICAL = "physical", "Physical asset"
    FACILITY = "facility", "Facility"
    TEAM = "team", "Team"
    PLATFORM = "platform", "Platform"
    OTHER = "other", "Other"


class AvailabilityStatus(models.TextChoices):
    PLANNED = "planned", "Planned"
    READY = "ready", "Ready"
    CONSTRAINED = "constrained", "Constrained"
    UNAVAILABLE = "unavailable", "Unavailable"


class ExerciseType(models.TextChoices):
    TABLETOP = "tabletop", "Tabletop"
    SIMULATION = "simulation", "Simulation"
    LIVE_DRILL = "live_drill", "Live drill"


class StandardType(models.TextChoices):
    ISP_EQUIPMENT = "isp_equipment", "ISP equipment"
    BANKING_EQUIPMENT = "banking_equipment", "Banking equipment"
    CNI_PROTECTION = "cni_protection", "CNI protection"
    PRIVACY = "privacy", "Data protection and privacy"
    CONFORMITY = "conformity", "Conformity assessment"


class TrainingType(models.TextChoices):
    RISK_MANAGEMENT = "risk_management", "Risk management"
    CONTINGENCY_RESPONSE = "contingency_response", "Contingency response"
    AUDIT_AWARENESS = "audit_awareness", "Audit and awareness"
    STANDARDS_COMPLIANCE = "standards_compliance", "Standards compliance"
    STAKEHOLDER_ENGAGEMENT = "stakeholder_engagement", "Stakeholder engagement"


class DeliveryMode(models.TextChoices):
    IN_PERSON = "in_person", "In person"
    VIRTUAL = "virtual", "Virtual"
    HYBRID = "hybrid", "Hybrid"


class DeliverableCategory(models.TextChoices):
    REPORT = "report", "Report"
    WORKSHOP = "workshop", "Workshop"
    POLICY = "policy", "Policy"
    REGULATION = "regulation", "Regulation"
    MAPPING = "mapping", "Mapping"
    RISK_REGISTER = "risk_register", "Risk register"
    CONTINGENCY = "contingency", "Contingency"
    STANDARD = "standard", "Standard"
    AUDIT = "audit", "Audit"
    TRAINING = "training", "Training"
    TEMPLATE = "template", "Template"


class Sector(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_sectors")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.ACTIVE)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Stakeholder(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_stakeholders")
    name = models.CharField(max_length=255)
    stakeholder_type = models.CharField(max_length=50, choices=StakeholderType.choices, default=StakeholderType.GOVERNMENT)
    sector_ref = models.ForeignKey(
        Sector,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stakeholders",
    )
    sector = models.CharField(max_length=120, blank=True)
    focal_point = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    engagement_role = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.ACTIVE)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class CriticalInfrastructure(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_infrastructure")
    owner_stakeholder = models.ForeignKey(
        Stakeholder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_infrastructure",
    )
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    sector_ref = models.ForeignKey(
        Sector,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="critical_infrastructure",
    )
    sector = models.CharField(max_length=120)
    infrastructure_type = models.CharField(max_length=20, choices=InfrastructureType.choices, default=InfrastructureType.CII)
    owner_name = models.CharField(max_length=255, blank=True)
    essential_service = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    designation_status = models.CharField(max_length=50, choices=DesignationStatus.choices, default=DesignationStatus.IDENTIFIED)
    criticality_level = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    vulnerability_level = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    mapping_status = models.CharField(max_length=50, choices=MappingStatus.choices, default=MappingStatus.PLANNED)
    mission_assurance_status = models.CharField(max_length=50, choices=AssuranceStatus.choices, default=AssuranceStatus.PENDING)
    requires_nda = models.BooleanField(default=True)
    critical_asset = models.BooleanField(default=False)
    last_assessed_at = models.DateField(null=True, blank=True)
    risk_summary = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.ACTIVE)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class GovernanceArtifact(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_artifacts")
    owner_stakeholder = models.ForeignKey(
        Stakeholder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="governance_artifacts",
    )
    related_infrastructure = models.ForeignKey(
        CriticalInfrastructure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="governance_artifacts",
    )
    title = models.CharField(max_length=255)
    phase = models.CharField(max_length=30, choices=Phase.choices, default=Phase.GOVERNANCE)
    artifact_type = models.CharField(max_length=50, choices=ArtifactType.choices, default=ArtifactType.FRAMEWORK)
    version = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.DRAFT)
    document_reference = models.URLField(blank=True)
    summary = models.TextField(blank=True)
    next_review_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class DeskStudyReview(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_desk_studies")
    related_stakeholder = models.ForeignKey(
        Stakeholder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="desk_study_reviews",
    )
    related_infrastructure = models.ForeignKey(
        CriticalInfrastructure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="desk_study_reviews",
    )
    title = models.CharField(max_length=255)
    source_type = models.CharField(max_length=30, choices=DeskStudySourceType.choices, default=DeskStudySourceType.REPORT)
    document_owner = models.CharField(max_length=255, blank=True)
    scope = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)
    gap_summary = models.TextField(blank=True)
    recommendation_summary = models.TextField(blank=True)
    priority = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.PLANNED)
    due_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    next_action = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class StakeholderConsultation(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_consultations")
    stakeholder = models.ForeignKey(
        Stakeholder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="consultations",
    )
    related_infrastructure = models.ForeignKey(
        CriticalInfrastructure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="consultations",
    )
    title = models.CharField(max_length=255)
    consultation_type = models.CharField(max_length=30, choices=ConsultationType.choices, default=ConsultationType.WORKSHOP)
    engagement_channel = models.CharField(max_length=20, choices=EngagementChannel.choices, default=EngagementChannel.IN_PERSON)
    meeting_link = models.URLField(blank=True)
    dial_in_details = models.TextField(blank=True)
    meeting_location = models.CharField(max_length=255, blank=True)
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    objective = models.TextField(blank=True)
    agenda = models.TextField(blank=True)
    attendees = models.TextField(blank=True)
    planned_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=ConsultationStatus.choices, default=ConsultationStatus.DRAFT)
    focal_person = models.CharField(max_length=255, blank=True)
    outcome_summary = models.TextField(blank=True)
    minutes = models.TextField(blank=True)
    follow_up_actions = models.TextField(blank=True)
    next_follow_up_date = models.DateField(null=True, blank=True)
    start_reminder_sent_for = models.DateTimeField(null=True, blank=True)
    follow_up_reminder_sent_for = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.start_datetime:
            self.planned_date = self.start_datetime.date()
        if self.end_datetime and not self.completed_date:
            self.completed_date = self.end_datetime.date()
        super().save(*args, **kwargs)


class RiskRegisterEntry(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_risks")
    infrastructure = models.ForeignKey(
        CriticalInfrastructure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="risk_entries",
    )
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=120, blank=True)
    scenario = models.TextField(blank=True)
    likelihood = models.PositiveSmallIntegerField(null=True, blank=True)
    impact = models.PositiveSmallIntegerField(null=True, blank=True)
    risk_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    risk_level = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    treatment_status = models.CharField(max_length=30, choices=RiskTreatmentStatus.choices, default=RiskTreatmentStatus.IDENTIFIED)
    risk_owner = models.CharField(max_length=255, blank=True)
    response_plan = models.TextField(blank=True)
    response_deadline = models.DateField(null=True, blank=True)
    last_reviewed_at = models.DateField(null=True, blank=True)
    update_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class CapacityAssessment(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_capacity_assessments")
    infrastructure = models.ForeignKey(
        CriticalInfrastructure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="capacity_assessments",
    )
    stakeholder = models.ForeignKey(
        Stakeholder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="capacity_assessments",
    )
    title = models.CharField(max_length=255)
    scope = models.CharField(max_length=255, blank=True)
    assessment_area = models.CharField(max_length=255, blank=True)
    current_maturity = models.PositiveSmallIntegerField(null=True, blank=True)
    target_maturity = models.PositiveSmallIntegerField(null=True, blank=True)
    gap_level = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.PLANNED)
    lead_assessor = models.CharField(max_length=255, blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    baseline_summary = models.TextField(blank=True)
    gap_summary = models.TextField(blank=True)
    priority_actions = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class ContingencyPlan(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_contingency_plans")
    title = models.CharField(max_length=255)
    plan_type = models.CharField(max_length=30, choices=PlanType.choices, default=PlanType.NATIONAL)
    scope = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.DRAFT)
    communication_procedure = models.TextField(blank=True)
    coordination_mechanism = models.TextField(blank=True)
    information_sharing_protocol = models.TextField(blank=True)
    activation_trigger = models.TextField(blank=True)
    review_cycle = models.CharField(max_length=120, blank=True)
    next_review_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class EmergencyResponseAsset(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_emergency_assets")
    contingency_plan = models.ForeignKey(
        ContingencyPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="emergency_assets",
    )
    infrastructure = models.ForeignKey(
        CriticalInfrastructure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="emergency_assets",
    )
    name = models.CharField(max_length=255)
    asset_type = models.CharField(max_length=30, choices=EmergencyAssetType.choices, default=EmergencyAssetType.DIGITAL)
    priority = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    owner_stakeholder = models.ForeignKey(
        Stakeholder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="emergency_response_assets",
    )
    owner_name = models.CharField(max_length=255, blank=True)
    availability_status = models.CharField(max_length=30, choices=AvailabilityStatus.choices, default=AvailabilityStatus.PLANNED)
    location = models.CharField(max_length=255, blank=True)
    activation_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class SimulationExercise(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_simulation_exercises")
    contingency_plan = models.ForeignKey(
        ContingencyPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="simulation_exercises",
    )
    title = models.CharField(max_length=255)
    exercise_type = models.CharField(max_length=30, choices=ExerciseType.choices, default=ExerciseType.TABLETOP)
    planned_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.PLANNED)
    scenario = models.TextField(blank=True)
    participating_sectors = models.TextField(blank=True)
    findings = models.TextField(blank=True)
    lessons_learned = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class CyberStandard(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_standards")
    title = models.CharField(max_length=255)
    standard_type = models.CharField(max_length=50, choices=StandardType.choices, default=StandardType.ISP_EQUIPMENT)
    target_sector_ref = models.ForeignKey(
        Sector,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cyber_standards",
    )
    target_sector = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.DRAFT)
    version = models.CharField(max_length=50, blank=True)
    control_focus = models.TextField(blank=True)
    review_cycle = models.CharField(max_length=120, blank=True)
    owner_name = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)
    next_review_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class AuditFramework(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_audit_frameworks")
    related_standard = models.ForeignKey(
        CyberStandard,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_frameworks",
    )
    title = models.CharField(max_length=255)
    scope = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.DRAFT)
    audit_frequency = models.CharField(max_length=120, blank=True)
    compliance_focus = models.TextField(blank=True)
    incident_response_procedure = models.TextField(blank=True)
    recovery_procedure = models.TextField(blank=True)
    next_review_date = models.DateField(null=True, blank=True)
    review_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class TrainingProgram(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_training_programs")
    title = models.CharField(max_length=255)
    program_type = models.CharField(max_length=50, choices=TrainingType.choices, default=TrainingType.RISK_MANAGEMENT)
    target_audience = models.CharField(max_length=255, blank=True)
    duration_days = models.PositiveIntegerField(null=True, blank=True)
    delivery_mode = models.CharField(max_length=20, choices=DeliveryMode.choices, default=DeliveryMode.IN_PERSON)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.PLANNED)
    certificate_required = models.BooleanField(default=False)
    participant_target = models.PositiveIntegerField(null=True, blank=True)
    summary = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class DeliverableMilestone(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_milestones")
    title = models.CharField(max_length=255)
    phase = models.CharField(max_length=30, choices=Phase.choices, default=Phase.GOVERNANCE)
    deliverable_category = models.CharField(max_length=50, choices=DeliverableCategory.choices, default=DeliverableCategory.REPORT)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.DRAFT)
    planned_week = models.PositiveIntegerField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    owner_name = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class ActionPlanTask(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_action_plan_tasks")
    related_risk = models.ForeignKey(
        RiskRegisterEntry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="action_plan_tasks",
    )
    related_milestone = models.ForeignKey(
        DeliverableMilestone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="action_plan_tasks",
    )
    related_infrastructure = models.ForeignKey(
        CriticalInfrastructure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="action_plan_tasks",
    )
    title = models.CharField(max_length=255)
    workstream = models.CharField(max_length=255, blank=True)
    owner_name = models.CharField(max_length=255, blank=True)
    priority = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.PLANNED)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    success_metric = models.CharField(max_length=255, blank=True)
    blocker_summary = models.TextField(blank=True)
    progress_note = models.TextField(blank=True)
    next_step = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title