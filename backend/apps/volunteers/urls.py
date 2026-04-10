from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import VolunteerViewSet, SkillViewSet, AvailabilityViewSet

router = DefaultRouter()
router.register("volunteers", VolunteerViewSet, basename="volunteers")
router.register("skills", SkillViewSet, basename="skills")
router.register("availabilitys", AvailabilityViewSet, basename="availabilitys")

urlpatterns = [path("", include(router.urls))]
