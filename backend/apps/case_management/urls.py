from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, CaseFileViewSet, CaseEventViewSet

router = DefaultRouter()
router.register("clients", ClientViewSet, basename="clients")
router.register("case-filess", CaseFileViewSet, basename="case-filess")
router.register("case-events", CaseEventViewSet, basename="case-events")

urlpatterns = [path("", include(router.urls))]
