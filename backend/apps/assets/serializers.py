from rest_framework import serializers
from .models import AssetType, Asset, Assignment


class AssetTypeSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = AssetType
        fields = "__all__"


class AssetSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    asset_type_name = serializers.CharField(source="asset_type.name", read_only=True)

    class Meta:
        model = Asset
        fields = "__all__"


class AssignmentSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    asset_name = serializers.CharField(source="asset.name", read_only=True)
    assignee_name = serializers.CharField(source="assignee.full_name", read_only=True)

    class Meta:
        model = Assignment
        fields = "__all__"
