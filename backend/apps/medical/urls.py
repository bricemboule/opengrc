from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import MedicalRecordViewSet, ConsultationViewSet

router = DefaultRouter()
router.register("medical-records", MedicalRecordViewSet, basename="medical-records")
router.register("consultations", ConsultationViewSet, basename="consultations")

urlpatterns = [path("", include(router.urls))]
