from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, TripViewSet, MaintenanceViewSet

router = DefaultRouter()
router.register("vehicles", VehicleViewSet, basename="vehicles")
router.register("trips", TripViewSet, basename="trips")
router.register("maintenances", MaintenanceViewSet, basename="maintenances")

urlpatterns = [path("", include(router.urls))]
