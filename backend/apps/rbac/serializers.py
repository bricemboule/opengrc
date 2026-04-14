from django.contrib.auth.models import Permission
from rest_framework import serializers

from .models import Role


class PermissionSerializer(serializers.ModelSerializer):
    app_label = serializers.CharField(source="content_type.app_label", read_only=True)
    model = serializers.CharField(source="content_type.model", read_only=True)

    class Meta:
        model = Permission
        fields = ["id", "name", "codename", "app_label", "model"]


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True, source="permissions", required=False
    )

    class Meta:
        model = Role
        fields = ["id", "name", "code", "description", "permissions", "permission_ids", "created_at", "updated_at"]
