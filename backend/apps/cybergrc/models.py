from django.db import models
from django.utils import timezone

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


class DeploymentStatus(models.TextChoices):
    IDLE = "idle", "Idle"
    STAGED = "staged", "Staged"
    DEPLOYED = "deployed", "Deployed"
    RETURNING = "returning", "Returning"
    MAINTENANCE = "maintenance", "Maintenance"


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


class RequirementType(models.TextChoices):
    GOVERNANCE = "governance", "Governance"
    TECHNICAL = "technical", "Technical"
    OPERATIONAL = "operational", "Operational"
    LEGAL = "legal", "Legal"
    REPORTING = "reporting", "Reporting"


class ControlType(models.TextChoices):
    PREVENTIVE = "preventive", "Preventive"
    DETECTIVE = "detective", "Detective"
    CORRECTIVE = "corrective", "Corrective"
    DIRECTIVE = "directive", "Directive"


class ConformityLevel(models.TextChoices):
    CONFORMANT = "conformant", "Conformant"
    PARTIAL = "partial", "Partially conformant"
    NON_CONFORMANT = "non_conformant", "Non-conformant"
    NOT_APPLICABLE = "not_applicable", "Not applicable"


class EvidenceStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    AVAILABLE = "available", "Available"
    REVIEWED = "reviewed", "Reviewed"
    EXPIRED = "expired", "Expired"
    REJECTED = "rejected", "Rejected"


class EvidenceType(models.TextChoices):
    DOCUMENT = "document", "Document"
    SCREENSHOT = "screenshot", "Screenshot"
    TEST_RESULT = "test_result", "Test result"
    CONFIGURATION = "configuration", "Configuration"
    INTERVIEW = "interview", "Interview"
    LOG = "log", "Log"
    REPORT = "report", "Report"
    OTHER = "other", "Other"


class ChecklistStatus(models.TextChoices):
    PLANNED = "planned", "Planned"
    IN_PROGRESS = "in_progress", "In progress"
    BLOCKED = "blocked", "Blocked"
    COMPLETED = "completed", "Completed"
    SKIPPED = "skipped", "Skipped"


class FindingStatus(models.TextChoices):
    IDENTIFIED = "identified", "Identified"
    IN_REVIEW = "in_review", "In review"
    VALIDATED = "validated", "Validated"
    REMEDIATING = "remediating", "Remediating"
    RESOLVED = "resolved", "Resolved"
    CLOSED = "closed", "Closed"


class NonConformityStatus(models.TextChoices):
    OPEN = "open", "Open"
    IN_REVIEW = "in_review", "In review"
    ACCEPTED = "accepted", "Accepted"
    REMEDIATING = "remediating", "Remediating"
    RESOLVED = "resolved", "Resolved"
    CLOSED = "closed", "Closed"


class AssetInventoryType(models.TextChoices):
    SERVICE = "service", "Service"
    APPLICATION = "application", "Application"
    PLATFORM = "platform", "Platform"
    NETWORK = "network", "Network"
    FACILITY = "facility", "Facility"
    DATA = "data", "Data asset"
    TEAM = "team", "Team"
    PROCESS = "process", "Process"
    OTHER = "other", "Other"


class ThreatType(models.TextChoices):
    MALWARE = "malware", "Malware"
    PHISHING = "phishing", "Phishing"
    DDOS = "ddos", "DDoS"
    RANSOMWARE = "ransomware", "Ransomware"
    INSIDER = "insider", "Insider threat"
    SUPPLY_CHAIN = "supply_chain", "Supply chain"
    FRAUD = "fraud", "Fraud"
    PHYSICAL = "physical", "Physical threat"
    OTHER = "other", "Other"


class ThreatSourceType(models.TextChoices):
    MONITORING = "monitoring", "Monitoring"
    INTERNAL_REPORT = "internal_report", "Internal report"
    PARTNER = "partner", "Partner notification"
    VENDOR = "vendor", "Vendor notification"
    CERT = "cert", "CERT / CSIRT"
    PUBLIC_SOURCE = "public_source", "Public source"
    EXERCISE = "exercise", "Exercise"
    OTHER = "other", "Other"


class ThreatEventStatus(models.TextChoices):
    IDENTIFIED = "identified", "Identified"
    ANALYZING = "analyzing", "Analyzing"
    MONITORED = "monitored", "Monitored"
    MITIGATED = "mitigated", "Mitigated"
    CLOSED = "closed", "Closed"


class VulnerabilityStatus(models.TextChoices):
    IDENTIFIED = "identified", "Identified"
    VALIDATING = "validating", "Validating"
    REMEDIATING = "remediating", "Remediating"
    ACCEPTED = "accepted", "Accepted"
    RESOLVED = "resolved", "Resolved"
    CLOSED = "closed", "Closed"


class BulletinType(models.TextChoices):
    ADVISORY = "advisory", "Advisory"
    ALERT = "alert", "Alert"
    INCIDENT = "incident", "Incident bulletin"
    COORDINATION = "coordination", "Coordination note"
    WATCHLIST = "watchlist", "Watchlist"


class IndicatorType(models.TextChoices):
    IP = "ip", "IP address"
    DOMAIN = "domain", "Domain"
    URL = "url", "URL"
    EMAIL = "email", "Email address"
    HASH = "hash", "Hash"
    YARA = "yara", "YARA rule"
    FILE_NAME = "file_name", "File name"
    OTHER = "other", "Other"


class IndicatorStatus(models.TextChoices):
    NEW = "new", "New"
    ACTIVE = "active", "Active"
    MONITORING = "monitoring", "Monitoring"
    EXPIRED = "expired", "Expired"
    REVOKED = "revoked", "Revoked"


class DistributionGroupType(models.TextChoices):
    SECTOR = "sector", "Sector"
    INSTITUTION = "institution", "Institution"
    INCIDENT = "incident", "Incident"
    NATIONAL = "national", "National"
    PARTNER = "partner", "Partner"


class ShareChannel(models.TextChoices):
    PLATFORM = "platform", "Platform notification"
    EMAIL = "email", "Email"
    BRIEFING = "briefing", "Briefing"
    PHONE = "phone", "Phone"
    SMS = "sms", "SMS"
    DOCUMENT = "document", "Document"
    MEETING = "meeting", "Meeting"


class ShareStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PREPARED = "prepared", "Prepared"
    SHARED = "shared", "Shared"
    ACKNOWLEDGED = "acknowledged", "Acknowledged"
    CLOSED = "closed", "Closed"


class AcknowledgementStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    RECEIVED = "received", "Received"
    ACTIONED = "actioned", "Actioned"
    DECLINED = "declined", "Declined"


class DocumentType(models.TextChoices):
    REPORT = "report", "Operational report"
    BRIEF = "brief", "Briefing note"
    MINUTES = "minutes", "Meeting minutes"
    PLAN = "plan", "Plan package"
    STANDARD_PACK = "standard_pack", "Standards pack"
    DOSSIER = "dossier", "Final dossier"
    TEMPLATE = "template", "Template"


class DocumentFormat(models.TextChoices):
    MARKDOWN = "markdown", "Markdown"
    TEXT = "text", "Plain text"
    JSON = "json", "JSON snapshot"
    PDF = "pdf", "PDF"
    DOCX = "docx", "DOCX"


class DocumentStatus(models.TextChoices):
    GENERATED = "generated", "Generated"
    IN_REVIEW = "in_review", "In review"
    APPROVED = "approved", "Approved"
    SUPERSEDED = "superseded", "Superseded"
    ARCHIVED = "archived", "Archived"


class ReviewCycleStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    ACTIVE = "active", "Active"
    OVERDUE = "overdue", "Overdue"
    COMPLETED = "completed", "Completed"
    ARCHIVED = "archived", "Archived"


class ReviewDecision(models.TextChoices):
    APPROVED = "approved", "Approved"
    CHANGES_REQUESTED = "changes_requested", "Changes requested"
    SUPERSEDED = "superseded", "Superseded"
    REJECTED = "rejected", "Rejected"


class ChangeType(models.TextChoices):
    GENERATED = "generated", "Generated"
    REVIEW_STARTED = "review_started", "Review started"
    REVIEW_RECORDED = "review_recorded", "Review recorded"
    APPROVED = "approved", "Approved"
    UPDATED = "updated", "Updated"
    SUPERSEDED = "superseded", "Superseded"
    REMINDER = "reminder", "Reminder"
    ARCHIVED = "archived", "Archived"


class RiskReviewDecision(models.TextChoices):
    ACCEPT = "accept", "Accept"
    MITIGATE = "mitigate", "Mitigate"
    ESCALATE = "escalate", "Escalate"
    MONITOR = "monitor", "Monitor"
    CLOSE = "close", "Close"


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
    geometry_geojson = models.JSONField(null=True, blank=True)
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
    deployment_status = models.CharField(max_length=30, choices=DeploymentStatus.choices, default=DeploymentStatus.IDLE)
    mobilization_eta_minutes = models.PositiveIntegerField(null=True, blank=True)
    capacity_units = models.PositiveIntegerField(null=True, blank=True)
    last_readiness_check = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    geometry_geojson = models.JSONField(null=True, blank=True)
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


class StandardRequirement(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_standard_requirements")
    related_standard = models.ForeignKey(
        CyberStandard,
        on_delete=models.CASCADE,
        related_name="requirements",
    )
    code = models.CharField(max_length=80)
    title = models.CharField(max_length=255)
    chapter = models.CharField(max_length=120, blank=True)
    requirement_type = models.CharField(max_length=30, choices=RequirementType.choices, default=RequirementType.TECHNICAL)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.DRAFT)
    priority = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    implementation_guidance = models.TextField(blank=True)
    verification_method = models.TextField(blank=True)
    owner_name = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=1)
    summary = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["related_standard_id", "sort_order", "-id"]
        constraints = [
            models.UniqueConstraint(fields=["organization", "related_standard", "code"], name="cybergrc_std_requirement_code_unique"),
        ]

    def __str__(self):
        return self.title


class StandardControl(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_standard_controls")
    related_standard = models.ForeignKey(
        CyberStandard,
        on_delete=models.CASCADE,
        related_name="controls",
    )
    related_requirement = models.ForeignKey(
        StandardRequirement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="controls",
    )
    code = models.CharField(max_length=80)
    title = models.CharField(max_length=255)
    domain = models.CharField(max_length=120, blank=True)
    control_type = models.CharField(max_length=30, choices=ControlType.choices, default=ControlType.PREVENTIVE)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.DRAFT)
    priority = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    control_objective = models.TextField(blank=True)
    control_procedure = models.TextField(blank=True)
    measurement_criteria = models.TextField(blank=True)
    owner_name = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["related_standard_id", "sort_order", "-id"]
        constraints = [
            models.UniqueConstraint(fields=["organization", "related_standard", "code"], name="cybergrc_std_control_code_unique"),
        ]

    def __str__(self):
        return self.title


class ConformityAssessment(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_conformity_assessments")
    related_standard = models.ForeignKey(
        CyberStandard,
        on_delete=models.CASCADE,
        related_name="conformity_assessments",
    )
    related_requirement = models.ForeignKey(
        StandardRequirement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="conformity_assessments",
    )
    related_control = models.ForeignKey(
        StandardControl,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="conformity_assessments",
    )
    related_framework = models.ForeignKey(
        AuditFramework,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="conformity_assessments",
    )
    target_stakeholder = models.ForeignKey(
        Stakeholder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="conformity_assessments",
    )
    related_infrastructure = models.ForeignKey(
        CriticalInfrastructure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="conformity_assessments",
    )
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.PLANNED)
    conformity_level = models.CharField(max_length=30, choices=ConformityLevel.choices, default=ConformityLevel.PARTIAL)
    assessed_on = models.DateField(null=True, blank=True)
    next_review_date = models.DateField(null=True, blank=True)
    assessor_name = models.CharField(max_length=255, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    evidence_summary = models.TextField(blank=True)
    gap_summary = models.TextField(blank=True)
    recommendation_summary = models.TextField(blank=True)
    follow_up_action = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-assessed_on", "-created_at", "-id"]

    def __str__(self):
        return self.title


class ControlEvidence(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_control_evidence")
    related_assessment = models.ForeignKey(
        ConformityAssessment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evidence_items",
    )
    related_standard = models.ForeignKey(
        CyberStandard,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evidence_items",
    )
    related_requirement = models.ForeignKey(
        StandardRequirement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evidence_items",
    )
    related_control = models.ForeignKey(
        StandardControl,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evidence_items",
    )
    title = models.CharField(max_length=255)
    evidence_type = models.CharField(max_length=30, choices=EvidenceType.choices, default=EvidenceType.DOCUMENT)
    status = models.CharField(max_length=30, choices=EvidenceStatus.choices, default=EvidenceStatus.PENDING)
    reference_url = models.URLField(blank=True)
    reference_label = models.CharField(max_length=255, blank=True)
    captured_on = models.DateField(null=True, blank=True)
    validity_until = models.DateField(null=True, blank=True)
    owner_name = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-captured_on", "-created_at", "-id"]

    def __str__(self):
        return self.title


class AuditPlan(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_audit_plans")
    related_framework = models.ForeignKey(
        AuditFramework,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_plans",
    )
    related_standard = models.ForeignKey(
        CyberStandard,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_plans",
    )
    target_stakeholder = models.ForeignKey(
        Stakeholder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_plans",
    )
    related_infrastructure = models.ForeignKey(
        CriticalInfrastructure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_plans",
    )
    title = models.CharField(max_length=255)
    scope = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.PLANNED)
    planned_start_date = models.DateField(null=True, blank=True)
    planned_end_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    lead_auditor = models.CharField(max_length=255, blank=True)
    objectives = models.TextField(blank=True)
    sampling_strategy = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    next_step = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-planned_start_date", "-created_at", "-id"]

    def __str__(self):
        return self.title


class AuditChecklist(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_audit_checklists")
    audit_plan = models.ForeignKey(
        AuditPlan,
        on_delete=models.CASCADE,
        related_name="checklist_items",
    )
    related_requirement = models.ForeignKey(
        StandardRequirement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_checklists",
    )
    related_control = models.ForeignKey(
        StandardControl,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_checklists",
    )
    item_order = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=255)
    verification_procedure = models.TextField(blank=True)
    expected_evidence = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=ChecklistStatus.choices, default=ChecklistStatus.PLANNED)
    result = models.CharField(max_length=30, choices=ConformityLevel.choices, blank=True)
    finding_summary = models.TextField(blank=True)
    evidence_reference = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["audit_plan_id", "item_order", "-id"]
        constraints = [
            models.UniqueConstraint(fields=["audit_plan", "item_order"], name="cybergrc_audit_checklist_item_order_unique"),
        ]

    def __str__(self):
        return self.title


class AuditFinding(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_audit_findings")
    audit_plan = models.ForeignKey(
        AuditPlan,
        on_delete=models.CASCADE,
        related_name="findings",
    )
    checklist_item = models.ForeignKey(
        AuditChecklist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="findings",
    )
    related_assessment = models.ForeignKey(
        ConformityAssessment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_findings",
    )
    related_requirement = models.ForeignKey(
        StandardRequirement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_findings",
    )
    related_control = models.ForeignKey(
        StandardControl,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_findings",
    )
    title = models.CharField(max_length=255)
    severity = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    status = models.CharField(max_length=30, choices=FindingStatus.choices, default=FindingStatus.IDENTIFIED)
    due_date = models.DateField(null=True, blank=True)
    owner_name = models.CharField(max_length=255, blank=True)
    impact_summary = models.TextField(blank=True)
    recommendation = models.TextField(blank=True)
    evidence_reference = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-due_date", "-created_at", "-id"]

    def __str__(self):
        return self.title


class NonConformity(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_non_conformities")
    audit_finding = models.ForeignKey(
        AuditFinding,
        on_delete=models.CASCADE,
        related_name="non_conformities",
    )
    related_assessment = models.ForeignKey(
        ConformityAssessment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="non_conformities",
    )
    related_requirement = models.ForeignKey(
        StandardRequirement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="non_conformities",
    )
    related_control = models.ForeignKey(
        StandardControl,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="non_conformities",
    )
    title = models.CharField(max_length=255)
    severity = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    status = models.CharField(max_length=30, choices=NonConformityStatus.choices, default=NonConformityStatus.OPEN)
    due_date = models.DateField(null=True, blank=True)
    owner_name = models.CharField(max_length=255, blank=True)
    root_cause = models.TextField(blank=True)
    containment_action = models.TextField(blank=True)
    remediation_expectation = models.TextField(blank=True)
    verification_notes = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-due_date", "-created_at", "-id"]

    def __str__(self):
        return self.title


class CorrectiveAction(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_corrective_actions")
    related_finding = models.ForeignKey(
        AuditFinding,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="corrective_actions",
    )
    related_non_conformity = models.ForeignKey(
        NonConformity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="corrective_actions",
    )
    related_assessment = models.ForeignKey(
        ConformityAssessment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="corrective_actions",
    )
    related_control = models.ForeignKey(
        StandardControl,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="corrective_actions",
    )
    related_infrastructure = models.ForeignKey(
        CriticalInfrastructure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="corrective_actions",
    )
    title = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255, blank=True)
    priority = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.PLANNED)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    action_summary = models.TextField(blank=True)
    success_metric = models.CharField(max_length=255, blank=True)
    blocker_summary = models.TextField(blank=True)
    evidence_reference = models.URLField(blank=True)
    verification_notes = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-due_date", "-created_at", "-id"]

    def __str__(self):
        return self.title


class AssetInventoryItem(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_asset_inventory")
    owner_stakeholder = models.ForeignKey(
        Stakeholder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="asset_inventory_items",
    )
    related_infrastructure = models.ForeignKey(
        CriticalInfrastructure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="asset_inventory_items",
    )
    sector_ref = models.ForeignKey(
        Sector,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="asset_inventory_items",
    )
    code = models.CharField(max_length=80)
    name = models.CharField(max_length=255)
    asset_type = models.CharField(max_length=30, choices=AssetInventoryType.choices, default=AssetInventoryType.SERVICE)
    sector = models.CharField(max_length=120, blank=True)
    owner_name = models.CharField(max_length=255, blank=True)
    essential_function = models.CharField(max_length=255, blank=True)
    admin_area = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    geometry_geojson = models.JSONField(null=True, blank=True)
    criticality_level = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    dependency_summary = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.ACTIVE)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "code"],
                name="cybergrc_asset_inventory_code_unique",
            )
        ]

    def __str__(self):
        return self.name


class ThreatEvent(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_threat_events")
    reporting_stakeholder = models.ForeignKey(
        Stakeholder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reported_threat_events",
    )
    related_infrastructure = models.ForeignKey(
        CriticalInfrastructure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="threat_events",
    )
    asset_item = models.ForeignKey(
        AssetInventoryItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="threat_events",
    )
    title = models.CharField(max_length=255)
    threat_type = models.CharField(max_length=30, choices=ThreatType.choices, default=ThreatType.OTHER)
    threat_source_type = models.CharField(max_length=30, choices=ThreatSourceType.choices, default=ThreatSourceType.MONITORING)
    status = models.CharField(max_length=30, choices=ThreatEventStatus.choices, default=ThreatEventStatus.IDENTIFIED)
    severity = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    confidence_level = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    first_seen_at = models.DateTimeField(null=True, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    admin_area = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    geometry_geojson = models.JSONField(null=True, blank=True)
    suspected_actor = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)
    recommended_action = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class VulnerabilityRecord(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_vulnerability_records")
    related_infrastructure = models.ForeignKey(
        CriticalInfrastructure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vulnerability_records",
    )
    asset_item = models.ForeignKey(
        AssetInventoryItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vulnerability_records",
    )
    related_threat_event = models.ForeignKey(
        ThreatEvent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vulnerability_records",
    )
    title = models.CharField(max_length=255)
    vulnerability_type = models.CharField(max_length=120, blank=True)
    severity = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    status = models.CharField(max_length=30, choices=VulnerabilityStatus.choices, default=VulnerabilityStatus.IDENTIFIED)
    exploitability_level = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    discovered_on = models.DateField(null=True, blank=True)
    remediation_due_date = models.DateField(null=True, blank=True)
    owner_name = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)
    remediation_guidance = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class RiskScenario(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_risk_scenarios")
    risk_register_entry = models.ForeignKey(
        RiskRegisterEntry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="risk_scenarios",
    )
    related_infrastructure = models.ForeignKey(
        CriticalInfrastructure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="risk_scenarios",
    )
    asset_item = models.ForeignKey(
        AssetInventoryItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="risk_scenarios",
    )
    related_threat_event = models.ForeignKey(
        ThreatEvent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="risk_scenarios",
    )
    vulnerability_record = models.ForeignKey(
        VulnerabilityRecord,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="risk_scenarios",
    )
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.DRAFT)
    risk_level = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    treatment_status = models.CharField(max_length=30, choices=RiskTreatmentStatus.choices, default=RiskTreatmentStatus.IDENTIFIED)
    scenario_owner = models.CharField(max_length=255, blank=True)
    likelihood = models.PositiveSmallIntegerField(null=True, blank=True)
    impact = models.PositiveSmallIntegerField(null=True, blank=True)
    risk_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    scenario_summary = models.TextField(blank=True)
    business_impact = models.TextField(blank=True)
    response_plan = models.TextField(blank=True)
    review_due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class RiskAssessmentReview(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_risk_assessment_reviews")
    risk_scenario = models.ForeignKey(
        RiskScenario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )
    risk_register_entry = models.ForeignKey(
        RiskRegisterEntry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assessment_reviews",
    )
    reviewer_stakeholder = models.ForeignKey(
        Stakeholder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="risk_assessment_reviews",
    )
    title = models.CharField(max_length=255)
    review_date = models.DateField(null=True, blank=True)
    decision = models.CharField(max_length=20, choices=RiskReviewDecision.choices, default=RiskReviewDecision.MONITOR)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.PLANNED)
    residual_risk_level = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    summary = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class ThreatBulletin(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_threat_bulletins")
    related_threat_event = models.ForeignKey(
        ThreatEvent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bulletins",
    )
    related_infrastructure = models.ForeignKey(
        CriticalInfrastructure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="threat_bulletins",
    )
    target_sector_ref = models.ForeignKey(
        Sector,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="threat_bulletins",
    )
    title = models.CharField(max_length=255)
    bulletin_type = models.CharField(max_length=30, choices=BulletinType.choices, default=BulletinType.ADVISORY)
    severity = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.DRAFT)
    issued_on = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    target_sector = models.CharField(max_length=120, blank=True)
    summary = models.TextField(blank=True)
    recommended_actions = models.TextField(blank=True)
    source_reference = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class Indicator(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_indicators")
    related_bulletin = models.ForeignKey(
        ThreatBulletin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="indicators",
    )
    related_threat_event = models.ForeignKey(
        ThreatEvent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="indicators",
    )
    title = models.CharField(max_length=255)
    indicator_type = models.CharField(max_length=30, choices=IndicatorType.choices, default=IndicatorType.IP)
    value = models.CharField(max_length=255)
    status = models.CharField(max_length=30, choices=IndicatorStatus.choices, default=IndicatorStatus.NEW)
    confidence_level = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    first_seen_at = models.DateTimeField(null=True, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title or self.value


class DistributionGroup(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_distribution_groups")
    title = models.CharField(max_length=255)
    group_type = models.CharField(max_length=30, choices=DistributionGroupType.choices, default=DistributionGroupType.SECTOR)
    target_sector_ref = models.ForeignKey(
        Sector,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="distribution_groups",
    )
    target_sector = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=50, choices=WorkflowStatus.choices, default=WorkflowStatus.ACTIVE)
    distribution_notes = models.TextField(blank=True)
    stakeholders = models.ManyToManyField(Stakeholder, blank=True, related_name="distribution_groups")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class InformationShare(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_information_shares")
    related_bulletin = models.ForeignKey(
        ThreatBulletin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="information_shares",
    )
    related_threat_event = models.ForeignKey(
        ThreatEvent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="information_shares",
    )
    distribution_group = models.ForeignKey(
        DistributionGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="information_shares",
    )
    target_stakeholder = models.ForeignKey(
        Stakeholder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="information_shares",
    )
    title = models.CharField(max_length=255)
    share_channel = models.CharField(max_length=30, choices=ShareChannel.choices, default=ShareChannel.PLATFORM)
    status = models.CharField(max_length=30, choices=ShareStatus.choices, default=ShareStatus.DRAFT)
    shared_at = models.DateTimeField(null=True, blank=True)
    acknowledgement_due_date = models.DateField(null=True, blank=True)
    action_requested = models.TextField(blank=True)
    access_link = models.URLField(blank=True)
    message_summary = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class Acknowledgement(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_acknowledgements")
    information_share = models.ForeignKey(
        InformationShare,
        on_delete=models.CASCADE,
        related_name="acknowledgements",
    )
    stakeholder = models.ForeignKey(
        Stakeholder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="acknowledgements",
    )
    status = models.CharField(max_length=30, choices=AcknowledgementStatus.choices, default=AcknowledgementStatus.PENDING)
    responded_at = models.DateTimeField(null=True, blank=True)
    action_note = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.information_share} / {self.stakeholder or 'Pending stakeholder'}"


class GeneratedDocument(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_generated_documents")
    title = models.CharField(max_length=255)
    module_key = models.CharField(max_length=80, blank=True)
    module_label = models.CharField(max_length=120, blank=True)
    record_id = models.PositiveBigIntegerField(null=True, blank=True)
    record_title = models.CharField(max_length=255, blank=True)
    document_type = models.CharField(max_length=30, choices=DocumentType.choices, default=DocumentType.REPORT)
    output_format = models.CharField(max_length=20, choices=DocumentFormat.choices, default=DocumentFormat.MARKDOWN)
    status = models.CharField(max_length=30, choices=DocumentStatus.choices, default=DocumentStatus.GENERATED)
    version_number = models.PositiveIntegerField(default=1)
    version_label = models.CharField(max_length=24, blank=True)
    generated_on = models.DateTimeField(default=timezone.now)
    published_on = models.DateTimeField(null=True, blank=True)
    generated_by_name = models.CharField(max_length=255, blank=True)
    approved_by_name = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)
    content_text = models.TextField(blank=True)
    generated_file = models.FileField(upload_to="generated_documents/%Y/%m/", blank=True)
    mime_type = models.CharField(max_length=120, blank=True)
    file_size_bytes = models.PositiveIntegerField(null=True, blank=True)
    source_snapshot = models.JSONField(default=dict, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-generated_on", "-id"]

    def save(self, *args, **kwargs):
        if not self.version_label:
            self.version_label = f"v{self.version_number}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ReviewCycle(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_review_cycles")
    generated_document = models.ForeignKey(
        GeneratedDocument,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="review_cycles",
    )
    title = models.CharField(max_length=255)
    module_key = models.CharField(max_length=80, blank=True)
    module_label = models.CharField(max_length=120, blank=True)
    record_id = models.PositiveBigIntegerField(null=True, blank=True)
    record_title = models.CharField(max_length=255, blank=True)
    owner_name = models.CharField(max_length=255, blank=True)
    cadence_days = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=ReviewCycleStatus.choices, default=ReviewCycleStatus.ACTIVE)
    current_version_label = models.CharField(max_length=24, blank=True)
    last_review_date = models.DateField(null=True, blank=True)
    next_review_date = models.DateField(null=True, blank=True)
    scope_summary = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["next_review_date", "-id"]

    def __str__(self):
        return self.title


class ReviewRecord(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_review_records")
    review_cycle = models.ForeignKey(
        ReviewCycle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="review_records",
    )
    generated_document = models.ForeignKey(
        GeneratedDocument,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="review_records",
    )
    title = models.CharField(max_length=255)
    review_date = models.DateField(default=timezone.localdate)
    decision = models.CharField(max_length=30, choices=ReviewDecision.choices, default=ReviewDecision.APPROVED)
    status = models.CharField(max_length=30, choices=WorkflowStatus.choices, default=WorkflowStatus.COMPLETED)
    reviewer_name = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    next_review_date = models.DateField(null=True, blank=True)
    version_label = models.CharField(max_length=24, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-review_date", "-id"]

    def __str__(self):
        return self.title


class ChangeLogEntry(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="cybergrc_change_log_entries")
    generated_document = models.ForeignKey(
        GeneratedDocument,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="change_log_entries",
    )
    review_cycle = models.ForeignKey(
        ReviewCycle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="change_log_entries",
    )
    review_record = models.ForeignKey(
        ReviewRecord,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="change_log_entries",
    )
    title = models.CharField(max_length=255)
    module_key = models.CharField(max_length=80, blank=True)
    module_label = models.CharField(max_length=120, blank=True)
    record_id = models.PositiveBigIntegerField(null=True, blank=True)
    record_title = models.CharField(max_length=255, blank=True)
    change_type = models.CharField(max_length=30, choices=ChangeType.choices, default=ChangeType.UPDATED)
    version_label = models.CharField(max_length=24, blank=True)
    summary = models.TextField(blank=True)
    change_metadata = models.JSONField(default=dict, blank=True)
    changed_on = models.DateTimeField(default=timezone.now)
    changed_by_name = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-changed_on", "-id"]

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
