from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, PurchaseRequestViewSet, PurchaseOrderViewSet

router = DefaultRouter()
router.register("vendors", VendorViewSet, basename="vendors")
router.register("purchase-requests", PurchaseRequestViewSet, basename="purchase-requests")
router.register("purchase-orders", PurchaseOrderViewSet, basename="purchase-orders")

urlpatterns = [path("", include(router.urls))]
