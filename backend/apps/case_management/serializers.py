from rest_framework import serializers
from .models import Client, CaseFile, CaseEvent


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class CaseFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseFile
        fields = "__all__"


class CaseEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseEvent
        fields = "__all__"
