from rest_framework import serializers
from apps.core.serializers import AuditFieldsSerializerMixin
from .models import Activity, Project, Task

class ProjectSerializer(AuditFieldsSerializerMixin):
    class Meta:
        model = Project
        fields = "__all__"


class ActivitySerializer(AuditFieldsSerializerMixin):
    project_name = serializers.CharField(source="project.name", read_only=True)
    contact_person_name = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = "__all__"

    def get_contact_person_name(self, obj):
        return str(obj.contact_person) if obj.contact_person else ""

    def validate(self, attrs):
        project = attrs.get("project") or getattr(self.instance, "project", None)
        organization = attrs.get("organization") or getattr(self.instance, "organization", None)
        contact_person = attrs.get("contact_person", getattr(self.instance, "contact_person", None))
        start_date = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end_date = attrs.get("end_date", getattr(self.instance, "end_date", None))
        if project and organization and project.organization_id != organization.id:
            raise serializers.ValidationError({"project": "Le projet doit appartenir a la meme organisation."})
        if contact_person and organization and contact_person.organization_id != organization.id:
            raise serializers.ValidationError({"contact_person": "Le contact doit appartenir a la meme organisation."})
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({"end_date": "La date de fin doit etre posterieure a la date de debut."})
        return attrs


class TaskSerializer(AuditFieldsSerializerMixin):
    project_name = serializers.CharField(source="project.name", read_only=True)
    activity_name = serializers.CharField(source="activity.name", read_only=True)
    assigned_to_name = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = "__all__"

    def get_assigned_to_name(self, obj):
        return str(obj.assigned_to) if obj.assigned_to else ""

    def validate(self, attrs):
        project = attrs.get("project") or getattr(self.instance, "project", None)
        activity = attrs.get("activity", getattr(self.instance, "activity", None))
        organization = attrs.get("organization") or getattr(self.instance, "organization", None)
        assigned_to = attrs.get("assigned_to", getattr(self.instance, "assigned_to", None))
        if project and organization and project.organization_id != organization.id:
            raise serializers.ValidationError({"project": "Le projet doit appartenir a la meme organisation."})
        if activity:
            if organization and activity.organization_id != organization.id:
                raise serializers.ValidationError({"activity": "L'activite doit appartenir a la meme organisation."})
            if project and activity.project_id != project.id:
                raise serializers.ValidationError({"activity": "L'activite selectionnee n'appartient pas au projet."})
        if assigned_to and organization and assigned_to.organization_id != organization.id:
            raise serializers.ValidationError({"assigned_to": "Le responsable assigne doit appartenir a la meme organisation."})
        return attrs
