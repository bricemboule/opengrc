from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AssetTypeViewSet, AssetViewSet, AssignmentViewSet

router = DefaultRouter()
router.register("asset-types", AssetTypeViewSet, basename="asset-types")
router.register("assets", AssetViewSet, basename="assets")
router.register("assignments", AssignmentViewSet, basename="assignments")

urlpatterns = [path("", include(router.urls))]
