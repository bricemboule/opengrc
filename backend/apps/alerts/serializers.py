from rest_framework import serializers
from .models import Alert, CapMessage


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = "__all__"


class CapMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapMessage
        fields = "__all__"
