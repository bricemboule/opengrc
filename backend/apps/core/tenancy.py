class OrganizationScopedQuerySetMixin:
    organization_field = "organization"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset
        if not getattr(user, "organization_id", None):
            return queryset.none()
        return queryset.filter(**{f"{self.organization_field}_id": user.organization_id})
