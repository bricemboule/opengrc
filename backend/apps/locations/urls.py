from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, GeoJsonLayerViewSet, MapLayerViewSet

router = DefaultRouter()
router.register("locations", LocationViewSet, basename="locations")
router.register("geo-json-layers", GeoJsonLayerViewSet, basename="geo-json-layers")
router.register("map-layers", MapLayerViewSet, basename="map-layers")

urlpatterns = [path("", include(router.urls))]
