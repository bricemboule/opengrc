from rest_framework import serializers
from .models import Location, GeoJsonLayer, MapLayer


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class GeoJsonLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoJsonLayer
        fields = "__all__"


class MapLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapLayer
        fields = "__all__"
