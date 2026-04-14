from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ActionPlanTaskViewSet,
    AuditFrameworkViewSet,
    CapacityAssessmentViewSet,
    ContingencyPlanViewSet,
    CriticalInfrastructureViewSet,
    CyberGrcOverviewView,
    CyberStandardViewSet,
    DeliverableMilestoneViewSet,
    DeskStudyReviewViewSet,
    EmergencyResponseAssetViewSet,
    GovernanceArtifactViewSet,
    RiskRegisterEntryViewSet,
    SectorViewSet,
    SimulationExerciseViewSet,
    StakeholderConsultationViewSet,
    StakeholderViewSet,
    TrainingProgramViewSet,
)

router = DefaultRouter()
router.register("sectors", SectorViewSet, basename="cybergrc-sectors")
router.register("stakeholders", StakeholderViewSet, basename="cybergrc-stakeholders")
router.register("critical-infrastructure", CriticalInfrastructureViewSet, basename="cybergrc-critical-infrastructure")
router.register("governance-artifacts", GovernanceArtifactViewSet, basename="cybergrc-governance-artifacts")
router.register("desk-study-reviews", DeskStudyReviewViewSet, basename="cybergrc-desk-study-reviews")
router.register("stakeholder-consultations", StakeholderConsultationViewSet, basename="cybergrc-stakeholder-consultations")
router.register("risk-register", RiskRegisterEntryViewSet, basename="cybergrc-risk-register")
router.register("capacity-assessments", CapacityAssessmentViewSet, basename="cybergrc-capacity-assessments")
router.register("contingency-plans", ContingencyPlanViewSet, basename="cybergrc-contingency-plans")
router.register("emergency-response-assets", EmergencyResponseAssetViewSet, basename="cybergrc-emergency-response-assets")
router.register("simulation-exercises", SimulationExerciseViewSet, basename="cybergrc-simulation-exercises")
router.register("cyber-standards", CyberStandardViewSet, basename="cybergrc-cyber-standards")
router.register("audit-frameworks", AuditFrameworkViewSet, basename="cybergrc-audit-frameworks")
router.register("training-programs", TrainingProgramViewSet, basename="cybergrc-training-programs")
router.register("deliverable-milestones", DeliverableMilestoneViewSet, basename="cybergrc-deliverable-milestones")
router.register("action-plan-tasks", ActionPlanTaskViewSet, basename="cybergrc-action-plan-tasks")

urlpatterns = [
    path("overview/", CyberGrcOverviewView.as_view(), name="cybergrc-overview"),
    path("", include(router.urls)),
]