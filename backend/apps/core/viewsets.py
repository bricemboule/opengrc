from rest_framework.viewsets import ModelViewSet

from .action_permissions import ActionPermission
from .mixins import AuditLogMixin


class AuditModelViewSet(AuditLogMixin, ModelViewSet):
    def get_permissions(self):
        permission_classes = list(getattr(self, "permission_classes", []))
        if not any(isinstance(permission_class, type) and issubclass(permission_class, ActionPermission) for permission_class in permission_classes):
            permission_classes.append(ActionPermission)
        return [permission_class() for permission_class in permission_classes]


class SoftDeleteAuditModelViewSet(AuditModelViewSet):
    organization_field = "organization"

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        extra_data = {"created_by": user, "updated_by": user}
        if user and not user.is_superuser and getattr(user, "organization_id", None):
            fields = getattr(serializer.Meta, "fields", [])
            if fields == "__all__" or self.organization_field in fields:
                extra_data[self.organization_field] = user.organization
        instance = serializer.save(**extra_data)
        self.log_action("create", instance)

    def perform_update(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        instance = serializer.save(updated_by=user)
        self.log_action("update", instance)

    def perform_destroy(self, instance):
        self.log_action("delete", instance)
        instance.delete()
