from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, DashboardView, ProjectViewSet, TaskViewSet

router = DefaultRouter()
router.register("", ProjectViewSet, basename="projects")
router.register("activities", ActivityViewSet, basename="activities")
router.register("tasks", TaskViewSet, basename="tasks")

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="projects-dashboard"),
    path("", include(router.urls)),
]
