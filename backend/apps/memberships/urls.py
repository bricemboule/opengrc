from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import MemberViewSet, SubscriptionViewSet

router = DefaultRouter()
router.register("members", MemberViewSet, basename="members")
router.register("subscriptions", SubscriptionViewSet, basename="subscriptions")

urlpatterns = [path("", include(router.urls))]
