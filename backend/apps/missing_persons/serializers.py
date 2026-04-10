from rest_framework import serializers
from .models import MissingPerson, MissingPersonReport


class MissingPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingPerson
        fields = "__all__"


class MissingPersonReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingPersonReport
        fields = "__all__"
