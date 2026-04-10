from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ShelterViewSet, OccupancyViewSet, CheckinViewSet

router = DefaultRouter()
router.register("shelters", ShelterViewSet, basename="shelters")
router.register("occupancys", OccupancyViewSet, basename="occupancys")
router.register("checkins", CheckinViewSet, basename="checkins")

urlpatterns = [path("", include(router.urls))]
