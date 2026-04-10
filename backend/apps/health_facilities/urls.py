from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import HospitalViewSet, FacilityStatusViewSet

router = DefaultRouter()
router.register("hospitals", HospitalViewSet, basename="hospitals")
router.register("facility-statuss", FacilityStatusViewSet, basename="facility-statuss")

urlpatterns = [path("", include(router.urls))]
