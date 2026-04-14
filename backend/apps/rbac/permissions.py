from rest_framework.permissions import BasePermission

from apps.core.action_permissions import ActionPermission


class RolePermission(ActionPermission):
    permission_map = {
        "list": "rbac.view_role",
        "retrieve": "rbac.view_role",
        "create": "rbac.add_role",
        "update": "rbac.change_role",
        "partial_update": "rbac.change_role",
        "destroy": "rbac.delete_role",
    }


class PermissionCatalogPermission(BasePermission):
    required_permission = "auth.view_permission"

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated or not user.is_active:
            return False
        if user.is_superuser:
            return True
        return user.has_perm(self.required_permission)
