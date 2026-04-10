from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AlertViewSet, CapMessageViewSet

router = DefaultRouter()
router.register("alerts", AlertViewSet, basename="alerts")
router.register("cap-messages", CapMessageViewSet, basename="cap-messages")

urlpatterns = [path("", include(router.urls))]
