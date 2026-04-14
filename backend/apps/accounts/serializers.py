from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.rbac.models import Role

from .models import User


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    role_ids = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), many=True, source="roles", required=False)
    permissions = serializers.SerializerMethodField()
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "full_name",
            "phone",
            "is_staff",
            "is_active",
            "is_verified",
            "roles",
            "role_ids",
            "permissions",
            "organization",
            "organization_name",
            "password",
        ]
        extra_kwargs = {
            "username": {"required": False, "allow_blank": True},
        }

    def get_roles(self, obj):
        return list(obj.roles.values("id", "name", "code"))

    def get_permissions(self, obj):
        return sorted(list(obj.get_all_permissions()))

    def create(self, validated_data):
        password = validated_data.pop("password", "")
        if not password:
            raise serializers.ValidationError({"password": "Temporary password is required when creating a user."})
        if not validated_data.get("username") and validated_data.get("email"):
            validated_data["username"] = validated_data["email"]
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=["password"])
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", "")
        if validated_data.get("email") and not validated_data.get("username"):
            validated_data["username"] = validated_data["email"]
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=["password"])
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs["email"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("Account is disabled.")
        attrs["user"] = user
        return attrs


def build_login_payload(user):
    refresh = RefreshToken.for_user(user)
    return {"user": UserSerializer(user).data, "access": str(refresh.access_token), "refresh": str(refresh)}
