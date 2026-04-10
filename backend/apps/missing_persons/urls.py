from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import MissingPersonViewSet, MissingPersonReportViewSet

router = DefaultRouter()
router.register("missing-persons", MissingPersonViewSet, basename="missing-persons")
router.register("missing-person-reports", MissingPersonReportViewSet, basename="missing-person-reports")

urlpatterns = [path("", include(router.urls))]
