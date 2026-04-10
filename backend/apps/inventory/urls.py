from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import WarehouseViewSet, StockViewSet, ShipmentViewSet, AdjustmentViewSet

router = DefaultRouter()
router.register("warehouses", WarehouseViewSet, basename="warehouses")
router.register("stocks", StockViewSet, basename="stocks")
router.register("shipments", ShipmentViewSet, basename="shipments")
router.register("adjustments", AdjustmentViewSet, basename="adjustments")

urlpatterns = [path("", include(router.urls))]
