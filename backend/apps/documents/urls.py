from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, FileAttachmentViewSet

router = DefaultRouter()
router.register("documents", DocumentViewSet, basename="documents")
router.register("file-attachments", FileAttachmentViewSet, basename="file-attachments")

urlpatterns = [path("", include(router.urls))]
