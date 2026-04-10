from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import VictimViewSet, IdentificationViewSet

router = DefaultRouter()
router.register("victims", VictimViewSet, basename="victims")
router.register("identifications", IdentificationViewSet, basename="identifications")

urlpatterns = [path("", include(router.urls))]
