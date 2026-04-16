from django.contrib import admin

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
    RiskRegisterEntry,
    SimulationExercise,
    Stakeholder,
    StakeholderConsultation,
    TrainingProgram,
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