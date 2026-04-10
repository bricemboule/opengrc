from rest_framework import serializers
from .models import Hospital, FacilityStatus


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"


class FacilityStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityStatus
        fields = "__all__"
