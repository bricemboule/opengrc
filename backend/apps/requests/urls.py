from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import RequestViewSet, RequestItemViewSet, RequestAssignmentViewSet

router = DefaultRouter()
router.register("requests", RequestViewSet, basename="requests")
router.register("request-items", RequestItemViewSet, basename="request-items")
router.register("request-assignments", RequestAssignmentViewSet, basename="request-assignments")

urlpatterns = [path("", include(router.urls))]
