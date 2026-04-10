from rest_framework import serializers
from .models import Request, RequestItem, RequestAssignment


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"


class RequestItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestItem
        fields = "__all__"


class RequestAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestAssignment
        fields = "__all__"
