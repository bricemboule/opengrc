from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import EpidemiologyCaseViewSet, ContactTraceViewSet, OutbreakViewSet

router = DefaultRouter()
router.register("epidemiology-cases", EpidemiologyCaseViewSet, basename="epidemiology-cases")
router.register("contact-traces", ContactTraceViewSet, basename="contact-traces")
router.register("outbreaks", OutbreakViewSet, basename="outbreaks")

urlpatterns = [path("", include(router.urls))]
