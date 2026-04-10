from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    FacilityTypeViewSet,
    FacilityViewSet,
    OfficeTypeViewSet,
    OrganizationTypeViewSet,
    OrganizationViewSet,
    SiteViewSet,
)

router = DefaultRouter()
router.register("", OrganizationViewSet, basename="organizations")
router.register("sites", SiteViewSet, basename="sites")
router.register("facilities", FacilityViewSet, basename="facilities")
router.register("organization-types", OrganizationTypeViewSet, basename="organization-types")
router.register("office-types", OfficeTypeViewSet, basename="office-types")
router.register("facility-types", FacilityTypeViewSet, basename="facility-types")

urlpatterns = [path("", include(router.urls))]
