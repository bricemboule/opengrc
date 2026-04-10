from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, DashboardViewSet, MetricViewSet

router = DefaultRouter()
router.register("reports", ReportViewSet, basename="reports")
router.register("dashboards", DashboardViewSet, basename="dashboards")
router.register("metrics", MetricViewSet, basename="metrics")

urlpatterns = [path("", include(router.urls))]
