from rest_framework import serializers
from .models import Event, Scenario, EventResource


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = "__all__"


class EventResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventResource
        fields = "__all__"
