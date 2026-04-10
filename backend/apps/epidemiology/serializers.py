from rest_framework import serializers
from .models import EpidemiologyCase, ContactTrace, Outbreak


class EpidemiologyCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EpidemiologyCase
        fields = "__all__"


class ContactTraceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactTrace
        fields = "__all__"


class OutbreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outbreak
        fields = "__all__"
