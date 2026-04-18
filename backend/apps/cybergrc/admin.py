from django.contrib import admin

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
    RiskRegisterEntry,
    RiskScenario,
    ReviewCycle,
    ReviewRecord,
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


@admin.register(Stakeholder)
class StakeholderAdmin(admin.ModelAdmin):
    list_display = ("name", "stakeholder_type", "sector", "status", "organization")
    search_fields = ("name", "sector", "focal_point", "email")
    list_filter = ("stakeholder_type", "status", "sector")


@admin.register(CriticalInfrastructure)
class CriticalInfrastructureAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "sector", "infrastructure_type", "criticality_level", "mapping_status")
    search_fields = ("code", "name", "sector", "owner_name", "essential_service")
    list_filter = ("infrastructure_type", "designation_status", "criticality_level", "mapping_status")


@admin.register(GovernanceArtifact)
class GovernanceArtifactAdmin(admin.ModelAdmin):
    list_display = ("title", "phase", "artifact_type", "status", "version")
    search_fields = ("title", "summary", "version")
    list_filter = ("phase", "artifact_type", "status")


@admin.register(DeskStudyReview)
class DeskStudyReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "source_type", "priority", "status", "due_date")
    search_fields = ("title", "document_owner", "scope")
    list_filter = ("source_type", "priority", "status")


@admin.register(StakeholderConsultation)
class StakeholderConsultationAdmin(admin.ModelAdmin):
    list_display = ("title", "consultation_type", "engagement_channel", "start_datetime", "status", "next_follow_up_date")
    search_fields = ("title", "focal_person", "objective", "agenda", "attendees", "meeting_location")
    list_filter = ("consultation_type", "engagement_channel", "status")


@admin.register(RiskRegisterEntry)
class RiskRegisterEntryAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "risk_level", "treatment_status", "response_deadline")
    search_fields = ("title", "category", "risk_owner")
    list_filter = ("risk_level", "treatment_status")


@admin.register(AssetInventoryItem)
class AssetInventoryItemAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "asset_type", "criticality_level", "status")
    search_fields = ("code", "name", "owner_name", "sector", "location", "admin_area")
    list_filter = ("asset_type", "criticality_level", "status")


@admin.register(ThreatEvent)
class ThreatEventAdmin(admin.ModelAdmin):
    list_display = ("title", "threat_type", "status", "severity", "first_seen_at", "last_seen_at")
    search_fields = ("title", "suspected_actor", "summary", "location", "admin_area")
    list_filter = ("threat_type", "threat_source_type", "status", "severity")


@admin.register(VulnerabilityRecord)
class VulnerabilityRecordAdmin(admin.ModelAdmin):
    list_display = ("title", "vulnerability_type", "severity", "status", "remediation_due_date")
    search_fields = ("title", "vulnerability_type", "owner_name", "summary")
    list_filter = ("severity", "status", "exploitability_level")


@admin.register(RiskScenario)
class RiskScenarioAdmin(admin.ModelAdmin):
    list_display = ("title", "risk_level", "treatment_status", "status", "review_due_date")
    search_fields = ("title", "scenario_owner", "scenario_summary", "business_impact")
    list_filter = ("risk_level", "treatment_status", "status")


@admin.register(RiskAssessmentReview)
class RiskAssessmentReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "decision", "residual_risk_level", "status", "review_date", "follow_up_date")
    search_fields = ("title", "summary", "recommendations")
    list_filter = ("decision", "residual_risk_level", "status")


@admin.register(ThreatBulletin)
class ThreatBulletinAdmin(admin.ModelAdmin):
    list_display = ("title", "bulletin_type", "severity", "status", "issued_on", "valid_until")
    search_fields = ("title", "summary", "target_sector")
    list_filter = ("bulletin_type", "severity", "status")


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ("title", "indicator_type", "status", "value", "first_seen_at", "last_seen_at")
    search_fields = ("title", "value", "notes")
    list_filter = ("indicator_type", "status", "confidence_level")


@admin.register(DistributionGroup)
class DistributionGroupAdmin(admin.ModelAdmin):
    list_display = ("title", "group_type", "target_sector", "status")
    search_fields = ("title", "target_sector", "distribution_notes")
    list_filter = ("group_type", "status")
    filter_horizontal = ("stakeholders",)


@admin.register(InformationShare)
class InformationShareAdmin(admin.ModelAdmin):
    list_display = ("title", "share_channel", "status", "shared_at", "acknowledgement_due_date")
    search_fields = ("title", "message_summary", "action_requested")
    list_filter = ("share_channel", "status")


@admin.register(Acknowledgement)
class AcknowledgementAdmin(admin.ModelAdmin):
    list_display = ("information_share", "stakeholder", "status", "responded_at")
    search_fields = ("information_share__title", "stakeholder__name", "action_note")
    list_filter = ("status",)


@admin.register(GeneratedDocument)
class GeneratedDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "module_label", "document_type", "status", "version_label", "generated_on")
    search_fields = ("title", "module_key", "module_label", "record_title", "summary")
    list_filter = ("document_type", "output_format", "status")


@admin.register(ReviewCycle)
class ReviewCycleAdmin(admin.ModelAdmin):
    list_display = ("title", "module_label", "status", "current_version_label", "next_review_date")
    search_fields = ("title", "module_key", "module_label", "record_title", "owner_name")
    list_filter = ("status",)


@admin.register(ReviewRecord)
class ReviewRecordAdmin(admin.ModelAdmin):
    list_display = ("title", "decision", "status", "reviewer_name", "review_date", "next_review_date")
    search_fields = ("title", "reviewer_name", "summary", "recommendations")
    list_filter = ("decision", "status")


@admin.register(ChangeLogEntry)
class ChangeLogEntryAdmin(admin.ModelAdmin):
    list_display = ("title", "change_type", "version_label", "changed_by_name", "changed_on")
    search_fields = ("title", "module_key", "module_label", "record_title", "summary", "changed_by_name")
    list_filter = ("change_type",)


@admin.register(CapacityAssessment)
class CapacityAssessmentAdmin(admin.ModelAdmin):
    list_display = ("title", "assessment_area", "gap_level", "status", "due_date")
    search_fields = ("title", "assessment_area", "lead_assessor")
    list_filter = ("gap_level", "status")


@admin.register(ContingencyPlan)
class ContingencyPlanAdmin(admin.ModelAdmin):
    list_display = ("title", "plan_type", "status", "next_review_date")
    search_fields = ("title", "scope")
    list_filter = ("plan_type", "status")


@admin.register(EmergencyResponseAsset)
class EmergencyResponseAssetAdmin(admin.ModelAdmin):
    list_display = ("name", "asset_type", "priority", "availability_status")
    search_fields = ("name", "owner_name", "location")
    list_filter = ("asset_type", "priority", "availability_status")


@admin.register(SimulationExercise)
class SimulationExerciseAdmin(admin.ModelAdmin):
    list_display = ("title", "exercise_type", "planned_date", "completed_date", "status")
    search_fields = ("title", "scenario")
    list_filter = ("exercise_type", "status")


@admin.register(CyberStandard)
class CyberStandardAdmin(admin.ModelAdmin):
    list_display = ("title", "standard_type", "target_sector", "status", "version")
    search_fields = ("title", "target_sector", "owner_name")
    list_filter = ("standard_type", "status")


@admin.register(AuditFramework)
class AuditFrameworkAdmin(admin.ModelAdmin):
    list_display = ("title", "scope", "status", "audit_frequency", "next_review_date")
    search_fields = ("title", "scope", "audit_frequency")
    list_filter = ("status",)


@admin.register(StandardRequirement)
class StandardRequirementAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "related_standard", "requirement_type", "status", "priority")
    search_fields = ("code", "title", "chapter", "owner_name")
    list_filter = ("requirement_type", "status", "priority")


@admin.register(StandardControl)
class StandardControlAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "related_standard", "control_type", "status", "priority")
    search_fields = ("code", "title", "domain", "owner_name")
    list_filter = ("control_type", "status", "priority")


@admin.register(ConformityAssessment)
class ConformityAssessmentAdmin(admin.ModelAdmin):
    list_display = ("title", "related_standard", "conformity_level", "status", "assessed_on", "next_review_date")
    search_fields = ("title", "assessor_name", "gap_summary")
    list_filter = ("conformity_level", "status")


@admin.register(ControlEvidence)
class ControlEvidenceAdmin(admin.ModelAdmin):
    list_display = ("title", "related_standard", "status", "captured_on", "validity_until")
    search_fields = ("title", "owner_name", "reference_label")
    list_filter = ("evidence_type", "status")


@admin.register(AuditPlan)
class AuditPlanAdmin(admin.ModelAdmin):
    list_display = ("title", "related_framework", "status", "planned_start_date", "planned_end_date")
    search_fields = ("title", "scope", "lead_auditor")
    list_filter = ("status",)


@admin.register(AuditChecklist)
class AuditChecklistAdmin(admin.ModelAdmin):
    list_display = ("title", "audit_plan", "status", "result", "item_order")
    search_fields = ("title", "verification_procedure", "expected_evidence")
    list_filter = ("status", "result")


@admin.register(AuditFinding)
class AuditFindingAdmin(admin.ModelAdmin):
    list_display = ("title", "audit_plan", "severity", "status", "due_date")
    search_fields = ("title", "owner_name", "recommendation")
    list_filter = ("severity", "status")


@admin.register(NonConformity)
class NonConformityAdmin(admin.ModelAdmin):
    list_display = ("title", "audit_finding", "severity", "status", "due_date")
    search_fields = ("title", "owner_name", "root_cause")
    list_filter = ("severity", "status")


@admin.register(CorrectiveAction)
class CorrectiveActionAdmin(admin.ModelAdmin):
    list_display = ("title", "owner_name", "priority", "status", "due_date", "completed_date")
    search_fields = ("title", "owner_name", "success_metric")
    list_filter = ("priority", "status")


@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "program_type", "delivery_mode", "status", "duration_days")
    search_fields = ("title", "target_audience")
    list_filter = ("program_type", "delivery_mode", "status")


@admin.register(DeliverableMilestone)
class DeliverableMilestoneAdmin(admin.ModelAdmin):
    list_display = ("title", "phase", "deliverable_category", "status", "planned_week", "due_date")
    search_fields = ("title", "owner_name")
    list_filter = ("phase", "deliverable_category", "status")


@admin.register(ActionPlanTask)
class ActionPlanTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "workstream", "priority", "status", "due_date")
    search_fields = ("title", "owner_name", "workstream")
    list_filter = ("priority", "status")
