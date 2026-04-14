from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MessageViewSet, NotificationViewSet

router = DefaultRouter()
router.register("notifications", NotificationViewSet, basename="notifications")
router.register("messages", MessageViewSet, basename="messages")

urlpatterns = [path("", include(router.urls))]
