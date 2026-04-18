from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from apps.core.serializers import AuditFieldsSerializerMixin

from .models import (
    AssetAllocation,
    Incident,
    IncidentAssignment,
    IncidentAttachment,
    IncidentCommunication,
    SOPExecution,
    SOPExecutionStep,
    SOPStep,
    SOPTemplate,
    IncidentTask,
    IncidentUpdate,
)


def validate_same_organization(attrs, instance, relation_names):
    organization = attrs.get("organization") or getattr(instance, "organization", None)
    errors = {}

    for relation_name in relation_names:
        related = attrs.get(relation_name, getattr(instance, relation_name, None))
        if related and organization and getattr(related, "organization_id", None) != organization.id:
            errors[relation_name] = "This selection must belong to the same organization."

    if errors:
        raise serializers.ValidationError(errors)


def validate_same_organization_many(attrs, instance, relation_names):
    organization = attrs.get("organization") or getattr(instance, "organization", None)
    errors = {}

    for relation_name in relation_names:
        related_items = attrs.get(relation_name)
        if related_items is None and instance is not None:
            related_items = getattr(instance, relation_name).all()

        if not related_items or not organization:
            continue

        invalid = [item for item in related_items if getattr(item, "organization_id", None) != organization.id]
        if invalid:
            errors[relation_name] = "All selected records must belong to the same organization."

    if errors:
        raise serializers.ValidationError(errors)


class IncidentSerializer(AuditFieldsSerializerMixin):
    incident_coordinator_name = serializers.SerializerMethodField()
    lead_stakeholder_name = serializers.CharField(source="lead_stakeholder.name", read_only=True)
    linked_plan_title = serializers.CharField(source="linked_plan.title", read_only=True)
    affected_sector_names = serializers.SerializerMethodField()
    affected_infrastructure_names = serializers.SerializerMethodField()

    class Meta:
        model = Incident
        fields = "__all__"

    def get_incident_coordinator_name(self, obj):
        coordinator = getattr(obj, "incident_coordinator", None)
        if not coordinator:
            return ""
        return coordinator.full_name or coordinator.email

    def get_affected_sector_names(self, obj):
        return [item.name for item in obj.affected_sectors.all()]

    def get_affected_infrastructure_names(self, obj):
        return [item.name for item in obj.affected_infrastructure.all()]

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["incident_coordinator", "lead_stakeholder", "linked_plan"])
        validate_same_organization_many(attrs, self.instance, ["affected_sectors", "affected_infrastructure"])

        reported_at = attrs.get("reported_at", getattr(self.instance, "reported_at", None))
        detected_at = attrs.get("detected_at", getattr(self.instance, "detected_at", None))
        closed_at = attrs.get("closed_at", getattr(self.instance, "closed_at", None))
        next_update_due = attrs.get("next_update_due", getattr(self.instance, "next_update_due", None))
        status = attrs.get("status", getattr(self.instance, "status", None))
        severity = attrs.get("severity", getattr(self.instance, "severity", None))

        errors = {}

        if detected_at and reported_at and reported_at < detected_at:
            errors["reported_at"] = "The reported time cannot be earlier than the detected time."

        if closed_at and reported_at and closed_at < reported_at:
            errors["closed_at"] = "The closed time must be after the reported time."

        if status == "closed" and not closed_at:
            attrs["closed_at"] = timezone.now()

        if status != "closed":
            attrs["closed_at"] = None

        if severity in {"critical", "national"} and not attrs.get("incident_coordinator", getattr(self.instance, "incident_coordinator", None)):
            errors["incident_coordinator"] = "Assign an incident coordinator for critical or nationally significant incidents."

        if next_update_due and reported_at and next_update_due < reported_at:
            errors["next_update_due"] = "The next update cannot be earlier than the reported time."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class IncidentUpdateSerializer(AuditFieldsSerializerMixin):
    incident_title = serializers.CharField(source="incident.title", read_only=True)

    class Meta:
        model = IncidentUpdate
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["incident"])

        incident = attrs.get("incident", getattr(self.instance, "incident", None))
        recorded_at = attrs.get("recorded_at", getattr(self.instance, "recorded_at", None))
        errors = {}

        if incident and recorded_at and incident.reported_at and recorded_at < incident.reported_at:
            errors["recorded_at"] = "Updates cannot be recorded before the incident was reported."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class IncidentTaskSerializer(AuditFieldsSerializerMixin):
    incident_title = serializers.CharField(source="incident.title", read_only=True)
    assigned_to_name = serializers.SerializerMethodField()

    class Meta:
        model = IncidentTask
        fields = "__all__"

    def get_assigned_to_name(self, obj):
        assignee = getattr(obj, "assigned_to", None)
        if not assignee:
            return ""
        return assignee.full_name or assignee.email

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["incident", "assigned_to"])

        due_at = attrs.get("due_at", getattr(self.instance, "due_at", None))
        completed_at = attrs.get("completed_at", getattr(self.instance, "completed_at", None))
        status = attrs.get("status", getattr(self.instance, "status", None))
        errors = {}

        if status == "completed" and not completed_at:
            attrs["completed_at"] = timezone.now()

        if status != "completed":
            attrs["completed_at"] = None

        if status == "blocked" and not attrs.get("blocker_summary", getattr(self.instance, "blocker_summary", "")):
            errors["blocker_summary"] = "Add a blocker summary before marking a task as blocked."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class IncidentAssignmentSerializer(AuditFieldsSerializerMixin):
    incident_title = serializers.CharField(source="incident.title", read_only=True)
    assignee_name = serializers.SerializerMethodField()
    stakeholder_name = serializers.CharField(source="stakeholder.name", read_only=True)

    class Meta:
        model = IncidentAssignment
        fields = "__all__"

    def get_assignee_name(self, obj):
        assignee = getattr(obj, "assignee", None)
        if not assignee:
            return ""
        return assignee.full_name or assignee.email

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["incident", "assignee", "stakeholder"])

        assigned_at = attrs.get("assigned_at", getattr(self.instance, "assigned_at", None))
        acknowledged_at = attrs.get("acknowledged_at", getattr(self.instance, "acknowledged_at", None))
        released_at = attrs.get("released_at", getattr(self.instance, "released_at", None))
        status = attrs.get("status", getattr(self.instance, "status", None))
        errors = {}

        if not attrs.get("assignee", getattr(self.instance, "assignee", None)) and not attrs.get("stakeholder", getattr(self.instance, "stakeholder", None)):
            errors["assignee"] = "Select an assignee or stakeholder for the response role."

        if assigned_at and acknowledged_at and acknowledged_at < assigned_at:
            errors["acknowledged_at"] = "Acknowledgement cannot happen before assignment."

        if assigned_at and released_at and released_at < assigned_at:
            errors["released_at"] = "Release cannot happen before assignment."

        if status == "acknowledged" and not acknowledged_at:
            attrs["acknowledged_at"] = timezone.now()

        if status == "released" and not released_at:
            attrs["released_at"] = timezone.now()

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class IncidentCommunicationSerializer(AuditFieldsSerializerMixin):
    incident_title = serializers.CharField(source="incident.title", read_only=True)

    class Meta:
        model = IncidentCommunication
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["incident"])
        return attrs


class IncidentAttachmentSerializer(AuditFieldsSerializerMixin):
    incident_title = serializers.CharField(source="incident.title", read_only=True)

    class Meta:
        model = IncidentAttachment
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["incident"])
        return attrs


class SOPTemplateSerializer(AuditFieldsSerializerMixin):
    contingency_plan_title = serializers.CharField(source="contingency_plan.title", read_only=True)
    related_artifact_title = serializers.CharField(source="related_artifact.title", read_only=True)
    related_infrastructure_name = serializers.CharField(source="related_infrastructure.name", read_only=True)
    owner_stakeholder_name = serializers.CharField(source="owner_stakeholder.name", read_only=True)
    step_count = serializers.SerializerMethodField()

    class Meta:
        model = SOPTemplate
        fields = "__all__"

    def get_step_count(self, obj):
        return obj.steps.count()

    def validate(self, attrs):
        validate_same_organization(
            attrs,
            self.instance,
            ["contingency_plan", "related_artifact", "related_infrastructure", "owner_stakeholder"],
        )
        return attrs


class SOPStepSerializer(AuditFieldsSerializerMixin):
    template_title = serializers.CharField(source="template.title", read_only=True)
    default_assignee_name = serializers.SerializerMethodField()

    class Meta:
        model = SOPStep
        fields = "__all__"

    def get_default_assignee_name(self, obj):
        assignee = getattr(obj, "default_assignee", None)
        if not assignee:
            return ""
        return assignee.full_name or assignee.email

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["template", "default_assignee"])
        return attrs


class SOPExecutionSerializer(AuditFieldsSerializerMixin):
    incident_title = serializers.CharField(source="incident.title", read_only=True)
    template_title = serializers.CharField(source="template.title", read_only=True)
    execution_commander_name = serializers.SerializerMethodField()
    completion_ratio = serializers.SerializerMethodField()
    active_step_total = serializers.SerializerMethodField()

    class Meta:
        model = SOPExecution
        fields = "__all__"

    def get_execution_commander_name(self, obj):
        commander = getattr(obj, "execution_commander", None)
        if not commander:
            return ""
        return commander.full_name or commander.email

    def get_completion_ratio(self, obj):
        total = obj.steps.count()
        if not total:
            return 0
        completed = obj.steps.filter(status__in=["completed", "skipped"]).count()
        return round((completed / total) * 100, 1)

    def get_active_step_total(self, obj):
        return obj.steps.exclude(status__in=["completed", "skipped", "cancelled"]).count()

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["incident", "template", "execution_commander"])

        incident = attrs.get("incident", getattr(self.instance, "incident", None))
        template = attrs.get("template", getattr(self.instance, "template", None))
        started_at = attrs.get("started_at", getattr(self.instance, "started_at", None))
        target_completion_at = attrs.get("target_completion_at", getattr(self.instance, "target_completion_at", None))
        completed_at = attrs.get("completed_at", getattr(self.instance, "completed_at", None))
        status = attrs.get("status", getattr(self.instance, "status", None))
        errors = {}

        if incident and template and incident.organization_id != template.organization_id:
            errors["template"] = "This SOP template must belong to the same organization as the incident."

        if target_completion_at and started_at and target_completion_at < started_at:
            errors["target_completion_at"] = "The target completion time must be after the start time."

        if completed_at and started_at and completed_at < started_at:
            errors["completed_at"] = "The completion time must be after the start time."

        if template and status in {"active", "completed"} and not template.steps.exists():
            errors["template"] = "Add SOP template steps before starting or completing this execution."

        if status == "active" and not started_at:
            attrs["started_at"] = timezone.now()

        if status == "completed" and not completed_at:
            attrs["completed_at"] = timezone.now()

        if status != "completed":
            attrs["completed_at"] = None

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            execution = super().create(validated_data)
            template_steps = list(execution.template.steps.order_by("step_order", "id"))
            if template_steps:
                SOPExecutionStep.objects.bulk_create(
                    [
                        SOPExecutionStep(
                            organization=execution.organization,
                            execution=execution,
                            template_step=step,
                            step_order=step.step_order,
                            title=step.title,
                            instruction=step.instruction,
                            step_type=step.step_type,
                            is_required=step.is_required,
                            assigned_to=step.default_assignee,
                        )
                        for step in template_steps
                    ]
                )
            return execution


class SOPExecutionStepSerializer(AuditFieldsSerializerMixin):
    execution_title = serializers.CharField(source="execution.title", read_only=True)
    template_step_title = serializers.CharField(source="template_step.title", read_only=True)
    assigned_to_name = serializers.SerializerMethodField()
    completed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = SOPExecutionStep
        fields = "__all__"

    def get_assigned_to_name(self, obj):
        assignee = getattr(obj, "assigned_to", None)
        if not assignee:
            return ""
        return assignee.full_name or assignee.email

    def get_completed_by_name(self, obj):
        actor = getattr(obj, "completed_by", None)
        if not actor:
            return ""
        return actor.full_name or actor.email

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["execution", "template_step", "assigned_to", "completed_by"])

        status = attrs.get("status", getattr(self.instance, "status", None))
        started_at = attrs.get("started_at", getattr(self.instance, "started_at", None))
        completed_at = attrs.get("completed_at", getattr(self.instance, "completed_at", None))
        errors = {}

        if completed_at and started_at and completed_at < started_at:
            errors["completed_at"] = "The completion time must be after the start time."

        if status == "in_progress" and not started_at:
            attrs["started_at"] = timezone.now()

        if status == "completed" and not completed_at:
            attrs["completed_at"] = timezone.now()

        if status != "completed":
            attrs["completed_at"] = None

        if status == "blocked" and not attrs.get("blocker_summary", getattr(self.instance, "blocker_summary", "")):
            errors["blocker_summary"] = "Add a blocker summary before marking the step as blocked."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class AssetAllocationSerializer(AuditFieldsSerializerMixin):
    incident_title = serializers.CharField(source="incident.title", read_only=True)
    emergency_asset_name = serializers.CharField(source="emergency_asset.name", read_only=True)
    destination_infrastructure_name = serializers.CharField(source="destination_infrastructure.name", read_only=True)
    related_task_title = serializers.CharField(source="related_task.title", read_only=True)
    approved_by_name = serializers.SerializerMethodField()
    requested_by_name = serializers.SerializerMethodField()
    asset_location = serializers.CharField(source="emergency_asset.location", read_only=True)
    asset_availability_status = serializers.CharField(source="emergency_asset.availability_status", read_only=True)
    asset_deployment_status = serializers.CharField(source="emergency_asset.deployment_status", read_only=True)
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    sector = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()

    class Meta:
        model = AssetAllocation
        fields = "__all__"

    def get_approved_by_name(self, obj):
        approver = getattr(obj, "approved_by", None)
        if not approver:
            return ""
        return approver.full_name or approver.email

    def get_requested_by_name(self, obj):
        actor = getattr(obj, "requested_by", None)
        if not actor:
            return ""
        return actor.full_name or actor.email

    def get_latitude(self, obj):
        target = obj.destination_infrastructure or getattr(obj.emergency_asset, "infrastructure", None)
        return getattr(target, "latitude", None)

    def get_longitude(self, obj):
        target = obj.destination_infrastructure or getattr(obj.emergency_asset, "infrastructure", None)
        return getattr(target, "longitude", None)

    def get_location(self, obj):
        target = obj.destination_infrastructure or getattr(obj.emergency_asset, "infrastructure", None)
        return getattr(target, "location", None) or getattr(obj.emergency_asset, "location", "")

    def get_sector(self, obj):
        target = obj.destination_infrastructure or getattr(obj.emergency_asset, "infrastructure", None)
        return getattr(target, "sector", None) or ""

    def get_summary(self, obj):
        return obj.deployment_notes or f"{obj.emergency_asset.name} allocated to {obj.incident.title}."

    def validate(self, attrs):
        validate_same_organization(
            attrs,
            self.instance,
            ["incident", "emergency_asset", "destination_infrastructure", "related_task", "approved_by", "requested_by"],
        )

        emergency_asset = attrs.get("emergency_asset", getattr(self.instance, "emergency_asset", None))
        quantity_requested = attrs.get("quantity_requested", getattr(self.instance, "quantity_requested", None))
        quantity_allocated = attrs.get("quantity_allocated", getattr(self.instance, "quantity_allocated", None))
        requested_at = attrs.get("requested_at", getattr(self.instance, "requested_at", None))
        approved_at = attrs.get("approved_at", getattr(self.instance, "approved_at", None))
        mobilized_at = attrs.get("mobilized_at", getattr(self.instance, "mobilized_at", None))
        deployed_at = attrs.get("deployed_at", getattr(self.instance, "deployed_at", None))
        released_at = attrs.get("released_at", getattr(self.instance, "released_at", None))
        status = attrs.get("status", getattr(self.instance, "status", None))
        errors = {}

        if quantity_requested is not None and quantity_requested < 1:
            errors["quantity_requested"] = "Request at least one unit."

        if quantity_allocated is not None and quantity_allocated < 1:
            errors["quantity_allocated"] = "Allocate at least one unit."

        if quantity_requested and quantity_allocated and quantity_allocated > quantity_requested:
            errors["quantity_allocated"] = "Allocated quantity cannot exceed the requested quantity."

        if emergency_asset and quantity_allocated and emergency_asset.capacity_units and quantity_allocated > emergency_asset.capacity_units:
            errors["quantity_allocated"] = "Allocated quantity cannot exceed the asset capacity."

        if approved_at and requested_at and approved_at < requested_at:
            errors["approved_at"] = "Approval cannot happen before the request."

        if mobilized_at and requested_at and mobilized_at < requested_at:
            errors["mobilized_at"] = "Mobilization cannot happen before the request."

        if deployed_at and mobilized_at and deployed_at < mobilized_at:
            errors["deployed_at"] = "Deployment cannot happen before mobilization."

        if released_at and deployed_at and released_at < deployed_at:
            errors["released_at"] = "Release cannot happen before deployment."

        if status == "approved" and not approved_at:
            attrs["approved_at"] = timezone.now()
        if status == "mobilizing" and not mobilized_at:
            attrs["mobilized_at"] = timezone.now()
        if status == "deployed" and not deployed_at:
            attrs["deployed_at"] = timezone.now()
        if status == "released" and not released_at:
            attrs["released_at"] = timezone.now()
        if quantity_requested and not quantity_allocated:
            attrs["quantity_allocated"] = quantity_requested

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
