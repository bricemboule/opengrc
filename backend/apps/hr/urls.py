from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CertificateViewSet,
    DepartmentViewSet,
    JobTitleViewSet,
    StaffSkillViewSet,
    StaffViewSet,
    TeamMemberViewSet,
    TeamViewSet,
    TrainingCourseViewSet,
    TrainingEventViewSet,
    TrainingParticipantViewSet,
)

router = DefaultRouter()
router.register("departments", DepartmentViewSet, basename="departments")
router.register("job-titles", JobTitleViewSet, basename="job-titles")
router.register("staffs", StaffViewSet, basename="staffs")
router.register("teams", TeamViewSet, basename="teams")
router.register("team-members", TeamMemberViewSet, basename="team-members")
router.register("staff-skills", StaffSkillViewSet, basename="staff-skills")
router.register("training-courses", TrainingCourseViewSet, basename="training-courses")
router.register("training-events", TrainingEventViewSet, basename="training-events")
router.register("training-participants", TrainingParticipantViewSet, basename="training-participants")
router.register("certificates", CertificateViewSet, basename="certificates")

urlpatterns = [path("", include(router.urls))]
