from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, ScenarioViewSet, EventResourceViewSet

router = DefaultRouter()
router.register("events", EventViewSet, basename="events")
router.register("scenarios", ScenarioViewSet, basename="scenarios")
router.register("event-resources", EventResourceViewSet, basename="event-resources")

urlpatterns = [path("", include(router.urls))]
