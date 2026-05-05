from rest_framework import serializers


class CurrentUserOrganizationDefault:
    requires_context = True

    def __call__(self, serializer_field):
        request = serializer_field.context.get("request")
        return getattr(getattr(request, "user", None), "organization", None)


class AuditFieldsSerializerMixin(serializers.ModelSerializer):
    created_by_email = serializers.EmailField(source="created_by.email", read_only=True)
    updated_by_email = serializers.EmailField(source="updated_by.email", read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        organization_field = self.fields.get("organization")
        if organization_field is not None and not organization_field.read_only:
            organization_field.required = False
            organization_field.allow_null = True
            organization_field.default = CurrentUserOrganizationDefault()
