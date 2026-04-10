from rest_framework import serializers
from apps.core.serializers import AuditFieldsSerializerMixin
from .models import Contact, Identity, Person

class PersonSerializer(AuditFieldsSerializerMixin):
    class Meta:
        model = Person
        fields = "__all__"


class ContactSerializer(AuditFieldsSerializerMixin):
    person_name = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = "__all__"

    def get_person_name(self, obj):
        return str(obj.person)

    def validate(self, attrs):
        person = attrs.get("person") or getattr(self.instance, "person", None)
        organization = attrs.get("organization") or getattr(self.instance, "organization", None)
        if person and organization and person.organization_id != organization.id:
            raise serializers.ValidationError({"person": "La personne doit appartenir a la meme organisation."})
        return attrs


class IdentitySerializer(AuditFieldsSerializerMixin):
    person_name = serializers.SerializerMethodField()

    class Meta:
        model = Identity
        fields = "__all__"

    def get_person_name(self, obj):
        return str(obj.person)

    def validate(self, attrs):
        person = attrs.get("person") or getattr(self.instance, "person", None)
        organization = attrs.get("organization") or getattr(self.instance, "organization", None)
        valid_from = attrs.get("valid_from", getattr(self.instance, "valid_from", None))
        valid_until = attrs.get("valid_until", getattr(self.instance, "valid_until", None))
        if person and organization and person.organization_id != organization.id:
            raise serializers.ValidationError({"person": "La personne doit appartenir a la meme organisation."})
        if valid_from and valid_until and valid_until < valid_from:
            raise serializers.ValidationError({"valid_until": "La date de fin de validite doit etre posterieure a la date de debut."})
        return attrs
