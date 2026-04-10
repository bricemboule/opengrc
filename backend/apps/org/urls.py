from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import FacilityViewSet, OrganizationViewSet, SiteViewSet

router = DefaultRouter()
router.register("", OrganizationViewSet, basename="organizations")
router.register("sites", SiteViewSet, basename="sites")
router.register("facilities", FacilityViewSet, basename="facilities")

urlpatterns = [path("", include(router.urls))]
