from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet
from .models import Contact, Identity, Person
from .serializers import ContactSerializer, IdentitySerializer, PersonSerializer
from .permissions import ContactPermission, IdentityPermission, PersonPermission

class PersonViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Person.objects.select_related("organization").all()
    serializer_class = PersonSerializer
    permission_classes = [PersonPermission]
    search_fields = ["first_name", "last_name", "gender"]
    ordering_fields = ["id", "first_name", "last_name", "created_at"]


class ContactViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Contact.objects.select_related("organization", "person").all()
    serializer_class = ContactSerializer
    permission_classes = [ContactPermission]
    search_fields = ["person__first_name", "person__last_name", "contact_type", "value", "label"]
    ordering_fields = ["id", "priority", "contact_type", "created_at"]


class IdentityViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Identity.objects.select_related("organization", "person").all()
    serializer_class = IdentitySerializer
    permission_classes = [IdentityPermission]
    search_fields = ["person__first_name", "person__last_name", "document_type", "document_number", "issued_country"]
    ordering_fields = ["id", "document_type", "valid_from", "valid_until", "created_at"]
