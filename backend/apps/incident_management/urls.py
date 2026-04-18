from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AssetAllocationViewSet,
    IncidentAssignmentViewSet,
    IncidentAttachmentViewSet,
    IncidentCommunicationViewSet,
    IncidentOverviewView,
    IncidentTaskViewSet,
    IncidentUpdateViewSet,
    IncidentViewSet,
    SOPExecutionStepViewSet,
    SOPExecutionViewSet,
    SOPStepViewSet,
    SOPTemplateViewSet,
)

router = DefaultRouter()
router.register("incidents", IncidentViewSet, basename="incident-management-incidents")
router.register("incident-updates", IncidentUpdateViewSet, basename="incident-management-incident-updates")
router.register("incident-tasks", IncidentTaskViewSet, basename="incident-management-incident-tasks")
router.register("incident-assignments", IncidentAssignmentViewSet, basename="incident-management-incident-assignments")
router.register("incident-communications", IncidentCommunicationViewSet, basename="incident-management-incident-communications")
router.register("incident-attachments", IncidentAttachmentViewSet, basename="incident-management-incident-attachments")
router.register("sop-templates", SOPTemplateViewSet, basename="incident-management-sop-templates")
router.register("sop-steps", SOPStepViewSet, basename="incident-management-sop-steps")
router.register("sop-executions", SOPExecutionViewSet, basename="incident-management-sop-executions")
router.register("sop-execution-steps", SOPExecutionStepViewSet, basename="incident-management-sop-execution-steps")
router.register("asset-allocations", AssetAllocationViewSet, basename="incident-management-asset-allocations")

urlpatterns = [
    path("overview/", IncidentOverviewView.as_view(), name="incident-management-overview"),
    path("", include(router.urls)),
]
