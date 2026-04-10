from rest_framework.permissions import BasePermission

class ActionPermission(BasePermission):
    permission_map = {}

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        required = self.permission_map.get(view.action)
        if not required:
            return True
        return required in user.get_all_permissions()
