from rest_framework.permissions import BasePermission


class ActionPermission(BasePermission):
    permission_map = {}
    method_permission_map = {
        "GET": "view",
        "POST": "add",
        "PUT": "change",
        "PATCH": "change",
        "DELETE": "delete",
    }

    def get_explicit_permission(self, view):
        action = getattr(view, "action", None)
        if not action:
            return None
        return self.permission_map.get(action)

    def get_model(self, view):
        queryset = getattr(view, "queryset", None)
        if queryset is not None and hasattr(queryset, "model"):
            return queryset.model

        serializer_class = getattr(view, "serializer_class", None)
        return getattr(getattr(serializer_class, "Meta", None), "model", None)

    def get_required_permission(self, request, view):
        explicit_permission = self.get_explicit_permission(view)
        if explicit_permission:
            return explicit_permission

        permission_prefix = self.method_permission_map.get(request.method.upper())
        model = self.get_model(view)
        if not permission_prefix or model is None:
            return None

        return f"{model._meta.app_label}.{permission_prefix}_{model._meta.model_name}"

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated or not user.is_active:
            return False
        if user.is_superuser:
            return True

        required_permission = self.get_required_permission(request, view)
        if not required_permission:
            return True

        return user.has_perm(required_permission)
