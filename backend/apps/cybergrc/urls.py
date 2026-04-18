from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AcknowledgementViewSet,
    ActionPlanTaskViewSet,
    AssetInventoryItemViewSet,
    AuditFrameworkViewSet,
    AuditChecklistViewSet,
    AuditFindingViewSet,
    AuditPlanViewSet,
    CapacityAssessmentViewSet,
    ConformityAssessmentViewSet,
    ContingencyPlanViewSet,
    ControlEvidenceViewSet,
    CorrectiveActionViewSet,
    CriticalInfrastructureViewSet,
    CyberGrcOverviewView,
    CyberStandardViewSet,
    DeliverableMilestoneViewSet,
    DeskStudyReviewViewSet,
    DistributionGroupViewSet,
    EmergencyResponseAssetViewSet,
    GeneratedDocumentViewSet,
    GovernanceArtifactViewSet,
    IndicatorViewSet,
    InformationShareViewSet,
    ChangeLogEntryViewSet,
    NonConformityViewSet,
    RiskAssessmentReviewViewSet,
    RiskRegisterEntryViewSet,
    RiskScenarioViewSet,
    ReviewCycleViewSet,
    ReviewRecordViewSet,
    SectorViewSet,
    SimulationExerciseViewSet,
    StandardControlViewSet,
    StandardRequirementViewSet,
    StakeholderConsultationViewSet,
    StakeholderViewSet,
    ThreatBulletinViewSet,
    ThreatEventViewSet,
    TrainingProgramViewSet,
    VulnerabilityRecordViewSet,
)

router = DefaultRouter()
router.register("sectors", SectorViewSet, basename="cybergrc-sectors")
router.register("stakeholders", StakeholderViewSet, basename="cybergrc-stakeholders")
router.register("critical-infrastructure", CriticalInfrastructureViewSet, basename="cybergrc-critical-infrastructure")
router.register("governance-artifacts", GovernanceArtifactViewSet, basename="cybergrc-governance-artifacts")
router.register("desk-study-reviews", DeskStudyReviewViewSet, basename="cybergrc-desk-study-reviews")
router.register("stakeholder-consultations", StakeholderConsultationViewSet, basename="cybergrc-stakeholder-consultations")
router.register("asset-inventory", AssetInventoryItemViewSet, basename="cybergrc-asset-inventory")
router.register("risk-register", RiskRegisterEntryViewSet, basename="cybergrc-risk-register")
router.register("threat-events", ThreatEventViewSet, basename="cybergrc-threat-events")
router.register("vulnerability-records", VulnerabilityRecordViewSet, basename="cybergrc-vulnerability-records")
router.register("risk-scenarios", RiskScenarioViewSet, basename="cybergrc-risk-scenarios")
router.register("risk-assessment-reviews", RiskAssessmentReviewViewSet, basename="cybergrc-risk-assessment-reviews")
router.register("capacity-assessments", CapacityAssessmentViewSet, basename="cybergrc-capacity-assessments")
router.register("threat-bulletins", ThreatBulletinViewSet, basename="cybergrc-threat-bulletins")
router.register("indicators", IndicatorViewSet, basename="cybergrc-indicators")
router.register("distribution-groups", DistributionGroupViewSet, basename="cybergrc-distribution-groups")
router.register("information-shares", InformationShareViewSet, basename="cybergrc-information-shares")
router.register("acknowledgements", AcknowledgementViewSet, basename="cybergrc-acknowledgements")
router.register("generated-documents", GeneratedDocumentViewSet, basename="cybergrc-generated-documents")
router.register("review-cycles", ReviewCycleViewSet, basename="cybergrc-review-cycles")
router.register("review-records", ReviewRecordViewSet, basename="cybergrc-review-records")
router.register("change-log-entries", ChangeLogEntryViewSet, basename="cybergrc-change-log-entries")
router.register("contingency-plans", ContingencyPlanViewSet, basename="cybergrc-contingency-plans")
router.register("emergency-response-assets", EmergencyResponseAssetViewSet, basename="cybergrc-emergency-response-assets")
router.register("simulation-exercises", SimulationExerciseViewSet, basename="cybergrc-simulation-exercises")
router.register("cyber-standards", CyberStandardViewSet, basename="cybergrc-cyber-standards")
router.register("standard-requirements", StandardRequirementViewSet, basename="cybergrc-standard-requirements")
router.register("standard-controls", StandardControlViewSet, basename="cybergrc-standard-controls")
router.register("conformity-assessments", ConformityAssessmentViewSet, basename="cybergrc-conformity-assessments")
router.register("control-evidence", ControlEvidenceViewSet, basename="cybergrc-control-evidence")
router.register("audit-frameworks", AuditFrameworkViewSet, basename="cybergrc-audit-frameworks")
router.register("audit-plans", AuditPlanViewSet, basename="cybergrc-audit-plans")
router.register("audit-checklists", AuditChecklistViewSet, basename="cybergrc-audit-checklists")
router.register("audit-findings", AuditFindingViewSet, basename="cybergrc-audit-findings")
router.register("non-conformities", NonConformityViewSet, basename="cybergrc-non-conformities")
router.register("corrective-actions", CorrectiveActionViewSet, basename="cybergrc-corrective-actions")
router.register("training-programs", TrainingProgramViewSet, basename="cybergrc-training-programs")
router.register("deliverable-milestones", DeliverableMilestoneViewSet, basename="cybergrc-deliverable-milestones")
router.register("action-plan-tasks", ActionPlanTaskViewSet, basename="cybergrc-action-plan-tasks")

urlpatterns = [
    path("overview/", CyberGrcOverviewView.as_view(), name="cybergrc-overview"),
    path("", include(router.urls)),
]
