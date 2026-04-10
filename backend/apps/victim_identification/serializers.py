from rest_framework import serializers
from .models import Victim, Identification


class VictimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Victim
        fields = "__all__"


class IdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identification
        fields = "__all__"
