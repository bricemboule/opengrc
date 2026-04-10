from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, ReferralViewSet

router = DefaultRouter()
router.register("patients", PatientViewSet, basename="patients")
router.register("referrals", ReferralViewSet, basename="referrals")

urlpatterns = [path("", include(router.urls))]
