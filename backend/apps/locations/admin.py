from django.contrib import admin
from .models import Location, GeoJsonLayer, MapLayer


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    search_fields = ("id",)


@admin.register(GeoJsonLayer)
class GeoJsonLayerAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    search_fields = ("id",)


@admin.register(MapLayer)
class MapLayerAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    search_fields = ("id",)
