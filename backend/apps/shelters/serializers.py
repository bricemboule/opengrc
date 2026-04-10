from rest_framework import serializers
from .models import Shelter, Occupancy, Checkin


class ShelterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelter
        fields = "__all__"


class OccupancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupancy
        fields = "__all__"


class CheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkin
        fields = "__all__"
