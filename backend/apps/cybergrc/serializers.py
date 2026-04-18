from rest_framework import serializers

from apps.core.serializers import AuditFieldsSerializerMixin

from .spatial import normalize_point_payload
from .models import (
    Acknowledgement,
    ActionPlanTask,
    AssetInventoryItem,
    AuditFramework,
    AuditChecklist,
    AuditFinding,
    AuditPlan,
    CapacityAssessment,
    ConformityAssessment,
    ContingencyPlan,
    ControlEvidence,
    CorrectiveAction,
    CriticalInfrastructure,
    CyberStandard,
    DeliverableMilestone,
    DeskStudyReview,
    DistributionGroup,
    EmergencyResponseAsset,
    GovernanceArtifact,
    GeneratedDocument,
    Indicator,
    InformationShare,
    ChangeLogEntry,
    NonConformity,
    RiskAssessmentReview,
    RiskRegisterEntry,
    RiskScenario,
    ReviewCycle,
    ReviewDecision,
    ReviewRecord,
    Sector,
    SimulationExercise,
    StandardControl,
    StandardRequirement,
    Stakeholder,
    StakeholderConsultation,
    ThreatBulletin,
    ThreatEvent,
    TrainingProgram,
    VulnerabilityRecord,
)


def validate_same_organization(attrs, instance, relation_names):
    organization = attrs.get("organization") or getattr(instance, "organization", None)
    errors = {}

    for relation_name in relation_names:
        related = attrs.get(relation_name, getattr(instance, relation_name, None))
        if not related or not organization:
            continue

        if hasattr(related, "organization_id"):
            related_items = [related]
        elif hasattr(related, "all"):
            related_items = list(related.all())
        elif isinstance(related, (list, tuple, set)):
            related_items = list(related)
        else:
            related_items = [related]

        invalid = [item for item in related_items if getattr(item, "organization_id", None) != organization.id]
        if invalid:
            errors[relation_name] = "This selection must belong to the same organization."

    if errors:
        raise serializers.ValidationError(errors)


def apply_relation_name_fallback(attrs, instance, relation_name, target_field_name, source_attribute="name"):
    related = attrs.get(relation_name, getattr(instance, relation_name, None))
    if related:
        attrs[target_field_name] = getattr(related, source_attribute, "") or ""
    return attrs


def align_standard_relations(attrs, instance, *, standard_field="related_standard", requirement_field=None, control_field=None):
    standard = attrs.get(standard_field, getattr(instance, standard_field, None))
    requirement = attrs.get(requirement_field, getattr(instance, requirement_field, None)) if requirement_field else None
    control = attrs.get(control_field, getattr(instance, control_field, None)) if control_field else None
    errors = {}

    if requirement and not standard:
        standard = requirement.related_standard
        attrs[standard_field] = standard

    if control and not standard:
        standard = control.related_standard
        attrs[standard_field] = standard

    if standard and requirement and requirement.related_standard_id != standard.id:
        errors[requirement_field] = "This requirement must belong to the selected standard."

    if standard and control and control.related_standard_id != standard.id:
        errors[control_field] = "This control must belong to the selected standard."

    if requirement and control and control.related_requirement_id and control.related_requirement_id != requirement.id:
        errors[control_field] = "This control must align with the selected requirement."

    if errors:
        raise serializers.ValidationError(errors)

    return attrs


class SectorSerializer(AuditFieldsSerializerMixin):
    class Meta:
        model = Sector
        fields = "__all__"


class StakeholderSerializer(AuditFieldsSerializerMixin):
    sector_name = serializers.SerializerMethodField()

    class Meta:
        model = Stakeholder
        fields = "__all__"

    def get_sector_name(self, obj):
        return getattr(getattr(obj, "sector_ref", None), "name", None) or obj.sector or ""

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["sector_ref"])
        return attrs

    def create(self, validated_data):
        validated_data = apply_relation_name_fallback(validated_data, None, "sector_ref", "sector")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = apply_relation_name_fallback(validated_data, instance, "sector_ref", "sector")
        return super().update(instance, validated_data)


class CriticalInfrastructureSerializer(AuditFieldsSerializerMixin):
    owner_stakeholder_name = serializers.CharField(source="owner_stakeholder.name", read_only=True)
    sector_name = serializers.SerializerMethodField()

    class Meta:
        model = CriticalInfrastructure
        fields = "__all__"

    def get_sector_name(self, obj):
        return getattr(getattr(obj, "sector_ref", None), "name", None) or obj.sector or ""

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["owner_stakeholder", "sector_ref"])
        normalize_point_payload(attrs, self.instance)
        return attrs

    def create(self, validated_data):
        validated_data = apply_relation_name_fallback(validated_data, None, "owner_stakeholder", "owner_name")
        validated_data = apply_relation_name_fallback(validated_data, None, "sector_ref", "sector")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = apply_relation_name_fallback(validated_data, instance, "owner_stakeholder", "owner_name")
        validated_data = apply_relation_name_fallback(validated_data, instance, "sector_ref", "sector")
        return super().update(instance, validated_data)


class GovernanceArtifactSerializer(AuditFieldsSerializerMixin):
    owner_stakeholder_name = serializers.CharField(source="owner_stakeholder.name", read_only=True)
    related_infrastructure_name = serializers.CharField(source="related_infrastructure.name", read_only=True)

    class Meta:
        model = GovernanceArtifact
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["owner_stakeholder", "related_infrastructure"])
        return attrs


class DeskStudyReviewSerializer(AuditFieldsSerializerMixin):
    related_stakeholder_name = serializers.CharField(source="related_stakeholder.name", read_only=True)
    related_infrastructure_name = serializers.CharField(source="related_infrastructure.name", read_only=True)

    class Meta:
        model = DeskStudyReview
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["related_stakeholder", "related_infrastructure"])
        return attrs


class StakeholderConsultationSerializer(AuditFieldsSerializerMixin):
    stakeholder_name = serializers.CharField(source="stakeholder.name", read_only=True)
    related_infrastructure_name = serializers.CharField(source="related_infrastructure.name", read_only=True)

    class Meta:
        model = StakeholderConsultation
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["stakeholder", "related_infrastructure"])

        start_datetime = attrs.get("start_datetime", getattr(self.instance, "start_datetime", None))
        end_datetime = attrs.get("end_datetime", getattr(self.instance, "end_datetime", None))
        engagement_channel = attrs.get("engagement_channel", getattr(self.instance, "engagement_channel", ""))
        meeting_link = attrs.get("meeting_link", getattr(self.instance, "meeting_link", ""))
        dial_in_details = attrs.get("dial_in_details", getattr(self.instance, "dial_in_details", ""))
        status = attrs.get("status", getattr(self.instance, "status", ""))

        errors = {}

        if start_datetime and end_datetime and end_datetime <= start_datetime:
            errors["end_datetime"] = "The end time must be after the start time."

        if engagement_channel in {"video", "hybrid"} and not (meeting_link or dial_in_details):
            errors["meeting_link"] = "Add a meeting link or dial-in details for remote participation."

        if status in {"scheduled", "confirmed", "rescheduled"} and not start_datetime:
            errors["start_datetime"] = "Add a start time before moving this consultation into the meeting workflow."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class RiskRegisterEntrySerializer(AuditFieldsSerializerMixin):
    infrastructure_name = serializers.CharField(source="infrastructure.name", read_only=True)

    class Meta:
        model = RiskRegisterEntry
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["infrastructure"])
        return attrs


class CapacityAssessmentSerializer(AuditFieldsSerializerMixin):
    infrastructure_name = serializers.CharField(source="infrastructure.name", read_only=True)
    stakeholder_name = serializers.CharField(source="stakeholder.name", read_only=True)

    class Meta:
        model = CapacityAssessment
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["infrastructure", "stakeholder"])
        return attrs


class ContingencyPlanSerializer(AuditFieldsSerializerMixin):
    class Meta:
        model = ContingencyPlan
        fields = "__all__"


class EmergencyResponseAssetSerializer(AuditFieldsSerializerMixin):
    contingency_plan_title = serializers.CharField(source="contingency_plan.title", read_only=True)
    infrastructure_name = serializers.CharField(source="infrastructure.name", read_only=True)
    owner_stakeholder_name = serializers.CharField(source="owner_stakeholder.name", read_only=True)

    class Meta:
        model = EmergencyResponseAsset
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["contingency_plan", "infrastructure", "owner_stakeholder"])
        normalize_point_payload(attrs, self.instance)

        mobilization_eta_minutes = attrs.get("mobilization_eta_minutes", getattr(self.instance, "mobilization_eta_minutes", None))
        capacity_units = attrs.get("capacity_units", getattr(self.instance, "capacity_units", None))
        availability_status = attrs.get("availability_status", getattr(self.instance, "availability_status", None))
        deployment_status = attrs.get("deployment_status", getattr(self.instance, "deployment_status", None))
        errors = {}

        if mobilization_eta_minutes is not None and mobilization_eta_minutes < 0:
            errors["mobilization_eta_minutes"] = "Mobilization ETA must be zero or greater."

        if capacity_units is not None and capacity_units < 1:
            errors["capacity_units"] = "Capacity units must be at least 1."

        if deployment_status in {"deployed", "staged"} and availability_status == "unavailable":
            errors["deployment_status"] = "An unavailable asset cannot be staged or deployed."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        validated_data = apply_relation_name_fallback(validated_data, None, "owner_stakeholder", "owner_name")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = apply_relation_name_fallback(validated_data, instance, "owner_stakeholder", "owner_name")
        return super().update(instance, validated_data)


class SimulationExerciseSerializer(AuditFieldsSerializerMixin):
    contingency_plan_title = serializers.CharField(source="contingency_plan.title", read_only=True)

    class Meta:
        model = SimulationExercise
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["contingency_plan"])
        return attrs


class CyberStandardSerializer(AuditFieldsSerializerMixin):
    target_sector_name = serializers.SerializerMethodField()

    class Meta:
        model = CyberStandard
        fields = "__all__"

    def get_target_sector_name(self, obj):
        return getattr(getattr(obj, "target_sector_ref", None), "name", None) or obj.target_sector or ""

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["target_sector_ref"])
        return attrs

    def create(self, validated_data):
        validated_data = apply_relation_name_fallback(validated_data, None, "target_sector_ref", "target_sector")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = apply_relation_name_fallback(validated_data, instance, "target_sector_ref", "target_sector")
        return super().update(instance, validated_data)


class AuditFrameworkSerializer(AuditFieldsSerializerMixin):
    related_standard_title = serializers.CharField(source="related_standard.title", read_only=True)

    class Meta:
        model = AuditFramework
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["related_standard"])
        return attrs


class StandardRequirementSerializer(AuditFieldsSerializerMixin):
    related_standard_title = serializers.CharField(source="related_standard.title", read_only=True)

    class Meta:
        model = StandardRequirement
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["related_standard"])
        return attrs


class StandardControlSerializer(AuditFieldsSerializerMixin):
    related_standard_title = serializers.CharField(source="related_standard.title", read_only=True)
    related_requirement_title = serializers.CharField(source="related_requirement.title", read_only=True)

    class Meta:
        model = StandardControl
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["related_standard", "related_requirement"])
        align_standard_relations(attrs, self.instance, requirement_field="related_requirement", control_field=None)
        if attrs.get("related_requirement"):
            requirement = attrs["related_requirement"]
            standard = attrs.get("related_standard", getattr(self.instance, "related_standard", None))
            if standard and requirement.related_standard_id != standard.id:
                raise serializers.ValidationError({"related_requirement": "This requirement must belong to the selected standard."})
        return attrs


class ConformityAssessmentSerializer(AuditFieldsSerializerMixin):
    related_standard_title = serializers.CharField(source="related_standard.title", read_only=True)
    related_requirement_title = serializers.CharField(source="related_requirement.title", read_only=True)
    related_control_title = serializers.CharField(source="related_control.title", read_only=True)
    related_framework_title = serializers.CharField(source="related_framework.title", read_only=True)
    target_stakeholder_name = serializers.CharField(source="target_stakeholder.name", read_only=True)
    related_infrastructure_name = serializers.CharField(source="related_infrastructure.name", read_only=True)

    class Meta:
        model = ConformityAssessment
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(
            attrs,
            self.instance,
            ["related_standard", "related_requirement", "related_control", "related_framework", "target_stakeholder", "related_infrastructure"],
        )
        align_standard_relations(attrs, self.instance, requirement_field="related_requirement", control_field="related_control")

        score = attrs.get("score", getattr(self.instance, "score", None))
        if score is not None and score > 100:
            raise serializers.ValidationError({"score": "The score must be between 0 and 100."})

        return attrs


class ControlEvidenceSerializer(AuditFieldsSerializerMixin):
    related_assessment_title = serializers.CharField(source="related_assessment.title", read_only=True)
    related_standard_title = serializers.CharField(source="related_standard.title", read_only=True)
    related_requirement_title = serializers.CharField(source="related_requirement.title", read_only=True)
    related_control_title = serializers.CharField(source="related_control.title", read_only=True)

    class Meta:
        model = ControlEvidence
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(
            attrs,
            self.instance,
            ["related_assessment", "related_standard", "related_requirement", "related_control"],
        )
        align_standard_relations(attrs, self.instance, requirement_field="related_requirement", control_field="related_control")

        captured_on = attrs.get("captured_on", getattr(self.instance, "captured_on", None))
        validity_until = attrs.get("validity_until", getattr(self.instance, "validity_until", None))
        if captured_on and validity_until and validity_until < captured_on:
            raise serializers.ValidationError({"validity_until": "Validity must be after the capture date."})

        assessment = attrs.get("related_assessment", getattr(self.instance, "related_assessment", None))
        standard = attrs.get("related_standard", getattr(self.instance, "related_standard", None))
        if assessment and standard and assessment.related_standard_id != standard.id:
            raise serializers.ValidationError({"related_standard": "The evidence standard must match the linked assessment."})

        return attrs


class AuditPlanSerializer(AuditFieldsSerializerMixin):
    related_framework_title = serializers.CharField(source="related_framework.title", read_only=True)
    related_standard_title = serializers.CharField(source="related_standard.title", read_only=True)
    target_stakeholder_name = serializers.CharField(source="target_stakeholder.name", read_only=True)
    related_infrastructure_name = serializers.CharField(source="related_infrastructure.name", read_only=True)

    class Meta:
        model = AuditPlan
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["related_framework", "related_standard", "target_stakeholder", "related_infrastructure"])

        framework = attrs.get("related_framework", getattr(self.instance, "related_framework", None))
        standard = attrs.get("related_standard", getattr(self.instance, "related_standard", None))
        if framework and not standard and framework.related_standard_id:
            attrs["related_standard"] = framework.related_standard
            standard = framework.related_standard
        if framework and standard and framework.related_standard_id and framework.related_standard_id != standard.id:
            raise serializers.ValidationError({"related_standard": "The selected standard must match the audit framework."})

        start_date = attrs.get("planned_start_date", getattr(self.instance, "planned_start_date", None))
        end_date = attrs.get("planned_end_date", getattr(self.instance, "planned_end_date", None))
        actual_end_date = attrs.get("actual_end_date", getattr(self.instance, "actual_end_date", None))
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({"planned_end_date": "The planned end date must be after the planned start date."})
        if start_date and actual_end_date and actual_end_date < start_date:
            raise serializers.ValidationError({"actual_end_date": "The actual end date must be after the planned start date."})

        return attrs


class AuditChecklistSerializer(AuditFieldsSerializerMixin):
    audit_plan_title = serializers.CharField(source="audit_plan.title", read_only=True)
    related_requirement_title = serializers.CharField(source="related_requirement.title", read_only=True)
    related_control_title = serializers.CharField(source="related_control.title", read_only=True)

    class Meta:
        model = AuditChecklist
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["audit_plan", "related_requirement", "related_control"])

        audit_plan = attrs.get("audit_plan", getattr(self.instance, "audit_plan", None))
        requirement = attrs.get("related_requirement", getattr(self.instance, "related_requirement", None))
        control = attrs.get("related_control", getattr(self.instance, "related_control", None))
        errors = {}

        if audit_plan and requirement and audit_plan.related_standard_id and requirement.related_standard_id != audit_plan.related_standard_id:
            errors["related_requirement"] = "This requirement must belong to the standard linked to the audit plan."
        if audit_plan and control and audit_plan.related_standard_id and control.related_standard_id != audit_plan.related_standard_id:
            errors["related_control"] = "This control must belong to the standard linked to the audit plan."
        if requirement and control and control.related_requirement_id and control.related_requirement_id != requirement.id:
            errors["related_control"] = "This control must align with the selected requirement."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class AuditFindingSerializer(AuditFieldsSerializerMixin):
    audit_plan_title = serializers.CharField(source="audit_plan.title", read_only=True)
    checklist_item_title = serializers.CharField(source="checklist_item.title", read_only=True)
    related_assessment_title = serializers.CharField(source="related_assessment.title", read_only=True)
    related_requirement_title = serializers.CharField(source="related_requirement.title", read_only=True)
    related_control_title = serializers.CharField(source="related_control.title", read_only=True)

    class Meta:
        model = AuditFinding
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["audit_plan", "checklist_item", "related_assessment", "related_requirement", "related_control"])

        audit_plan = attrs.get("audit_plan", getattr(self.instance, "audit_plan", None))
        checklist_item = attrs.get("checklist_item", getattr(self.instance, "checklist_item", None))
        requirement = attrs.get("related_requirement", getattr(self.instance, "related_requirement", None))
        control = attrs.get("related_control", getattr(self.instance, "related_control", None))
        errors = {}

        if checklist_item and audit_plan and checklist_item.audit_plan_id != audit_plan.id:
            errors["checklist_item"] = "This checklist item must belong to the selected audit plan."
        if audit_plan and requirement and audit_plan.related_standard_id and requirement.related_standard_id != audit_plan.related_standard_id:
            errors["related_requirement"] = "This requirement must belong to the audit plan standard."
        if audit_plan and control and audit_plan.related_standard_id and control.related_standard_id != audit_plan.related_standard_id:
            errors["related_control"] = "This control must belong to the audit plan standard."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class NonConformitySerializer(AuditFieldsSerializerMixin):
    audit_finding_title = serializers.CharField(source="audit_finding.title", read_only=True)
    related_assessment_title = serializers.CharField(source="related_assessment.title", read_only=True)
    related_requirement_title = serializers.CharField(source="related_requirement.title", read_only=True)
    related_control_title = serializers.CharField(source="related_control.title", read_only=True)

    class Meta:
        model = NonConformity
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["audit_finding", "related_assessment", "related_requirement", "related_control"])
        return attrs


class CorrectiveActionSerializer(AuditFieldsSerializerMixin):
    related_finding_title = serializers.CharField(source="related_finding.title", read_only=True)
    related_non_conformity_title = serializers.CharField(source="related_non_conformity.title", read_only=True)
    related_assessment_title = serializers.CharField(source="related_assessment.title", read_only=True)
    related_control_title = serializers.CharField(source="related_control.title", read_only=True)
    related_infrastructure_name = serializers.CharField(source="related_infrastructure.name", read_only=True)

    class Meta:
        model = CorrectiveAction
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(
            attrs,
            self.instance,
            ["related_finding", "related_non_conformity", "related_assessment", "related_control", "related_infrastructure"],
        )

        start_date = attrs.get("start_date", getattr(self.instance, "start_date", None))
        due_date = attrs.get("due_date", getattr(self.instance, "due_date", None))
        completed_date = attrs.get("completed_date", getattr(self.instance, "completed_date", None))
        if start_date and due_date and due_date < start_date:
            raise serializers.ValidationError({"due_date": "The due date must be after the start date."})
        if start_date and completed_date and completed_date < start_date:
            raise serializers.ValidationError({"completed_date": "The completed date must be after the start date."})

        return attrs


class AssetInventoryItemSerializer(AuditFieldsSerializerMixin):
    owner_stakeholder_name = serializers.CharField(source="owner_stakeholder.name", read_only=True)
    related_infrastructure_name = serializers.CharField(source="related_infrastructure.name", read_only=True)
    sector_name = serializers.SerializerMethodField()

    class Meta:
        model = AssetInventoryItem
        fields = "__all__"

    def get_sector_name(self, obj):
        return getattr(getattr(obj, "sector_ref", None), "name", None) or obj.sector or ""

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["owner_stakeholder", "related_infrastructure", "sector_ref"])
        normalize_point_payload(attrs, self.instance)
        return attrs

    def create(self, validated_data):
        validated_data = apply_relation_name_fallback(validated_data, None, "owner_stakeholder", "owner_name")
        validated_data = apply_relation_name_fallback(validated_data, None, "sector_ref", "sector")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = apply_relation_name_fallback(validated_data, instance, "owner_stakeholder", "owner_name")
        validated_data = apply_relation_name_fallback(validated_data, instance, "sector_ref", "sector")
        return super().update(instance, validated_data)


class ThreatEventSerializer(AuditFieldsSerializerMixin):
    reporting_stakeholder_name = serializers.CharField(source="reporting_stakeholder.name", read_only=True)
    related_infrastructure_name = serializers.CharField(source="related_infrastructure.name", read_only=True)
    asset_item_name = serializers.CharField(source="asset_item.name", read_only=True)

    class Meta:
        model = ThreatEvent
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["reporting_stakeholder", "related_infrastructure", "asset_item"])
        normalize_point_payload(attrs, self.instance)

        first_seen_at = attrs.get("first_seen_at", getattr(self.instance, "first_seen_at", None))
        last_seen_at = attrs.get("last_seen_at", getattr(self.instance, "last_seen_at", None))
        related_infrastructure = attrs.get("related_infrastructure", getattr(self.instance, "related_infrastructure", None))
        asset_item = attrs.get("asset_item", getattr(self.instance, "asset_item", None))
        errors = {}

        if first_seen_at and last_seen_at and last_seen_at < first_seen_at:
            errors["last_seen_at"] = "The last seen time must be after the first seen time."

        if asset_item and not related_infrastructure and asset_item.related_infrastructure_id:
            attrs["related_infrastructure"] = asset_item.related_infrastructure
            related_infrastructure = asset_item.related_infrastructure

        if asset_item and related_infrastructure and asset_item.related_infrastructure_id and asset_item.related_infrastructure_id != related_infrastructure.id:
            errors["asset_item"] = "This asset item must belong to the selected infrastructure."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class VulnerabilityRecordSerializer(AuditFieldsSerializerMixin):
    related_infrastructure_name = serializers.CharField(source="related_infrastructure.name", read_only=True)
    asset_item_name = serializers.CharField(source="asset_item.name", read_only=True)
    related_threat_event_title = serializers.CharField(source="related_threat_event.title", read_only=True)

    class Meta:
        model = VulnerabilityRecord
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["related_infrastructure", "asset_item", "related_threat_event"])

        discovered_on = attrs.get("discovered_on", getattr(self.instance, "discovered_on", None))
        remediation_due_date = attrs.get("remediation_due_date", getattr(self.instance, "remediation_due_date", None))
        related_infrastructure = attrs.get("related_infrastructure", getattr(self.instance, "related_infrastructure", None))
        asset_item = attrs.get("asset_item", getattr(self.instance, "asset_item", None))
        threat_event = attrs.get("related_threat_event", getattr(self.instance, "related_threat_event", None))
        errors = {}

        if discovered_on and remediation_due_date and remediation_due_date < discovered_on:
            errors["remediation_due_date"] = "The remediation due date must be after the discovery date."

        if asset_item and not related_infrastructure and asset_item.related_infrastructure_id:
            attrs["related_infrastructure"] = asset_item.related_infrastructure
            related_infrastructure = asset_item.related_infrastructure

        if threat_event and not related_infrastructure and threat_event.related_infrastructure_id:
            attrs["related_infrastructure"] = threat_event.related_infrastructure
            related_infrastructure = threat_event.related_infrastructure

        if asset_item and related_infrastructure and asset_item.related_infrastructure_id and asset_item.related_infrastructure_id != related_infrastructure.id:
            errors["asset_item"] = "This asset item must belong to the selected infrastructure."

        if threat_event and related_infrastructure and threat_event.related_infrastructure_id and threat_event.related_infrastructure_id != related_infrastructure.id:
            errors["related_threat_event"] = "This threat event must belong to the selected infrastructure."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class RiskScenarioSerializer(AuditFieldsSerializerMixin):
    risk_register_entry_title = serializers.CharField(source="risk_register_entry.title", read_only=True)
    related_infrastructure_name = serializers.CharField(source="related_infrastructure.name", read_only=True)
    asset_item_name = serializers.CharField(source="asset_item.name", read_only=True)
    related_threat_event_title = serializers.CharField(source="related_threat_event.title", read_only=True)
    vulnerability_record_title = serializers.CharField(source="vulnerability_record.title", read_only=True)

    class Meta:
        model = RiskScenario
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(
            attrs,
            self.instance,
            ["risk_register_entry", "related_infrastructure", "asset_item", "related_threat_event", "vulnerability_record"],
        )

        related_infrastructure = attrs.get("related_infrastructure", getattr(self.instance, "related_infrastructure", None))
        asset_item = attrs.get("asset_item", getattr(self.instance, "asset_item", None))
        threat_event = attrs.get("related_threat_event", getattr(self.instance, "related_threat_event", None))
        vulnerability_record = attrs.get("vulnerability_record", getattr(self.instance, "vulnerability_record", None))
        risk_entry = attrs.get("risk_register_entry", getattr(self.instance, "risk_register_entry", None))
        errors = {}

        if not related_infrastructure:
            if asset_item and asset_item.related_infrastructure_id:
                attrs["related_infrastructure"] = asset_item.related_infrastructure
                related_infrastructure = asset_item.related_infrastructure
            elif threat_event and threat_event.related_infrastructure_id:
                attrs["related_infrastructure"] = threat_event.related_infrastructure
                related_infrastructure = threat_event.related_infrastructure
            elif vulnerability_record and vulnerability_record.related_infrastructure_id:
                attrs["related_infrastructure"] = vulnerability_record.related_infrastructure
                related_infrastructure = vulnerability_record.related_infrastructure
            elif risk_entry and risk_entry.infrastructure_id:
                attrs["related_infrastructure"] = risk_entry.infrastructure
                related_infrastructure = risk_entry.infrastructure

        if asset_item and related_infrastructure and asset_item.related_infrastructure_id and asset_item.related_infrastructure_id != related_infrastructure.id:
            errors["asset_item"] = "This asset item must belong to the selected infrastructure."
        if threat_event and related_infrastructure and threat_event.related_infrastructure_id and threat_event.related_infrastructure_id != related_infrastructure.id:
            errors["related_threat_event"] = "This threat event must belong to the selected infrastructure."
        if vulnerability_record and related_infrastructure and vulnerability_record.related_infrastructure_id and vulnerability_record.related_infrastructure_id != related_infrastructure.id:
            errors["vulnerability_record"] = "This vulnerability record must belong to the selected infrastructure."
        if risk_entry and related_infrastructure and risk_entry.infrastructure_id and risk_entry.infrastructure_id != related_infrastructure.id:
            errors["risk_register_entry"] = "This risk register entry must belong to the selected infrastructure."
        if vulnerability_record and threat_event and vulnerability_record.related_threat_event_id and vulnerability_record.related_threat_event_id != threat_event.id:
            errors["vulnerability_record"] = "This vulnerability record must align with the selected threat event."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class RiskAssessmentReviewSerializer(AuditFieldsSerializerMixin):
    risk_scenario_title = serializers.CharField(source="risk_scenario.title", read_only=True)
    risk_register_entry_title = serializers.CharField(source="risk_register_entry.title", read_only=True)
    reviewer_stakeholder_name = serializers.CharField(source="reviewer_stakeholder.name", read_only=True)

    class Meta:
        model = RiskAssessmentReview
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["risk_scenario", "risk_register_entry", "reviewer_stakeholder"])

        risk_scenario = attrs.get("risk_scenario", getattr(self.instance, "risk_scenario", None))
        risk_register_entry = attrs.get("risk_register_entry", getattr(self.instance, "risk_register_entry", None))
        review_date = attrs.get("review_date", getattr(self.instance, "review_date", None))
        follow_up_date = attrs.get("follow_up_date", getattr(self.instance, "follow_up_date", None))
        errors = {}

        if risk_scenario and not risk_register_entry and risk_scenario.risk_register_entry_id:
            attrs["risk_register_entry"] = risk_scenario.risk_register_entry
            risk_register_entry = risk_scenario.risk_register_entry

        if risk_scenario and risk_register_entry and risk_scenario.risk_register_entry_id and risk_scenario.risk_register_entry_id != risk_register_entry.id:
            errors["risk_register_entry"] = "This review must align with the selected risk scenario."

        if review_date and follow_up_date and follow_up_date < review_date:
            errors["follow_up_date"] = "The follow-up date must be after the review date."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class ThreatBulletinSerializer(AuditFieldsSerializerMixin):
    related_threat_event_title = serializers.CharField(source="related_threat_event.title", read_only=True)
    related_infrastructure_name = serializers.CharField(source="related_infrastructure.name", read_only=True)
    target_sector_name = serializers.SerializerMethodField()

    class Meta:
        model = ThreatBulletin
        fields = "__all__"

    def get_target_sector_name(self, obj):
        return getattr(getattr(obj, "target_sector_ref", None), "name", None) or obj.target_sector or ""

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["related_threat_event", "related_infrastructure", "target_sector_ref"])

        issued_on = attrs.get("issued_on", getattr(self.instance, "issued_on", None))
        valid_until = attrs.get("valid_until", getattr(self.instance, "valid_until", None))
        related_threat_event = attrs.get("related_threat_event", getattr(self.instance, "related_threat_event", None))
        related_infrastructure = attrs.get("related_infrastructure", getattr(self.instance, "related_infrastructure", None))
        errors = {}

        if issued_on and valid_until and valid_until < issued_on:
            errors["valid_until"] = "The validity end date must be after the issue date."

        if related_threat_event and not related_infrastructure and related_threat_event.related_infrastructure_id:
            attrs["related_infrastructure"] = related_threat_event.related_infrastructure
            related_infrastructure = related_threat_event.related_infrastructure

        if related_threat_event and related_infrastructure and related_threat_event.related_infrastructure_id and related_threat_event.related_infrastructure_id != related_infrastructure.id:
            errors["related_threat_event"] = "This threat event must belong to the selected infrastructure."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        validated_data = apply_relation_name_fallback(validated_data, None, "target_sector_ref", "target_sector")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = apply_relation_name_fallback(validated_data, instance, "target_sector_ref", "target_sector")
        return super().update(instance, validated_data)


class IndicatorSerializer(AuditFieldsSerializerMixin):
    related_bulletin_title = serializers.CharField(source="related_bulletin.title", read_only=True)
    related_threat_event_title = serializers.CharField(source="related_threat_event.title", read_only=True)

    class Meta:
        model = Indicator
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["related_bulletin", "related_threat_event"])

        related_bulletin = attrs.get("related_bulletin", getattr(self.instance, "related_bulletin", None))
        related_threat_event = attrs.get("related_threat_event", getattr(self.instance, "related_threat_event", None))
        first_seen_at = attrs.get("first_seen_at", getattr(self.instance, "first_seen_at", None))
        last_seen_at = attrs.get("last_seen_at", getattr(self.instance, "last_seen_at", None))
        errors = {}

        if first_seen_at and last_seen_at and last_seen_at < first_seen_at:
            errors["last_seen_at"] = "The last seen time must be after the first seen time."

        if related_bulletin and not related_threat_event and related_bulletin.related_threat_event_id:
            attrs["related_threat_event"] = related_bulletin.related_threat_event
            related_threat_event = related_bulletin.related_threat_event

        if related_bulletin and related_threat_event and related_bulletin.related_threat_event_id and related_bulletin.related_threat_event_id != related_threat_event.id:
            errors["related_threat_event"] = "This indicator must align with the selected bulletin."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class DistributionGroupSerializer(AuditFieldsSerializerMixin):
    target_sector_name = serializers.SerializerMethodField()
    stakeholder_names = serializers.SerializerMethodField()

    class Meta:
        model = DistributionGroup
        fields = "__all__"

    def get_target_sector_name(self, obj):
        return getattr(getattr(obj, "target_sector_ref", None), "name", None) or obj.target_sector or ""

    def get_stakeholder_names(self, obj):
        return [stakeholder.name for stakeholder in obj.stakeholders.all()]

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["target_sector_ref", "stakeholders"])
        return attrs

    def create(self, validated_data):
        validated_data = apply_relation_name_fallback(validated_data, None, "target_sector_ref", "target_sector")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = apply_relation_name_fallback(validated_data, instance, "target_sector_ref", "target_sector")
        return super().update(instance, validated_data)


class InformationShareSerializer(AuditFieldsSerializerMixin):
    related_bulletin_title = serializers.CharField(source="related_bulletin.title", read_only=True)
    related_threat_event_title = serializers.CharField(source="related_threat_event.title", read_only=True)
    distribution_group_title = serializers.CharField(source="distribution_group.title", read_only=True)
    target_stakeholder_name = serializers.CharField(source="target_stakeholder.name", read_only=True)

    class Meta:
        model = InformationShare
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(
            attrs,
            self.instance,
            ["related_bulletin", "related_threat_event", "distribution_group", "target_stakeholder"],
        )

        related_bulletin = attrs.get("related_bulletin", getattr(self.instance, "related_bulletin", None))
        related_threat_event = attrs.get("related_threat_event", getattr(self.instance, "related_threat_event", None))
        distribution_group = attrs.get("distribution_group", getattr(self.instance, "distribution_group", None))
        target_stakeholder = attrs.get("target_stakeholder", getattr(self.instance, "target_stakeholder", None))
        shared_at = attrs.get("shared_at", getattr(self.instance, "shared_at", None))
        acknowledgement_due_date = attrs.get("acknowledgement_due_date", getattr(self.instance, "acknowledgement_due_date", None))
        status = attrs.get("status", getattr(self.instance, "status", None))
        errors = {}

        if not distribution_group and not target_stakeholder:
            errors["distribution_group"] = "Select a distribution group or a direct target stakeholder."

        if related_bulletin and not related_threat_event and related_bulletin.related_threat_event_id:
            attrs["related_threat_event"] = related_bulletin.related_threat_event
            related_threat_event = related_bulletin.related_threat_event

        if related_bulletin and related_threat_event and related_bulletin.related_threat_event_id and related_bulletin.related_threat_event_id != related_threat_event.id:
            errors["related_threat_event"] = "This information share must align with the selected bulletin."

        if shared_at and acknowledgement_due_date and acknowledgement_due_date < shared_at.date():
            errors["acknowledgement_due_date"] = "The acknowledgement due date must be on or after the share time."

        if status in {"shared", "acknowledged", "closed"} and not shared_at:
            errors["shared_at"] = "Add the share time before moving this information share forward."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class AcknowledgementSerializer(AuditFieldsSerializerMixin):
    information_share_title = serializers.CharField(source="information_share.title", read_only=True)
    stakeholder_name = serializers.CharField(source="stakeholder.name", read_only=True)

    class Meta:
        model = Acknowledgement
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["information_share", "stakeholder"])
        return attrs


class GeneratedDocumentSerializer(AuditFieldsSerializerMixin):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = GeneratedDocument
        fields = "__all__"

    def get_download_url(self, obj):
        request = self.context.get("request")
        path = f"/api/cybergrc/generated-documents/{obj.id}/download/"
        return request.build_absolute_uri(path) if request else path

    def validate(self, attrs):
        generated_on = attrs.get("generated_on", getattr(self.instance, "generated_on", None))
        published_on = attrs.get("published_on", getattr(self.instance, "published_on", None))

        if generated_on and published_on and published_on < generated_on:
            raise serializers.ValidationError({"published_on": "The publication time must be after the generation time."})

        return attrs


class ReviewCycleSerializer(AuditFieldsSerializerMixin):
    generated_document_title = serializers.CharField(source="generated_document.title", read_only=True)

    class Meta:
        model = ReviewCycle
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["generated_document"])

        generated_document = attrs.get("generated_document", getattr(self.instance, "generated_document", None))
        last_review_date = attrs.get("last_review_date", getattr(self.instance, "last_review_date", None))
        next_review_date = attrs.get("next_review_date", getattr(self.instance, "next_review_date", None))

        if last_review_date and next_review_date and next_review_date < last_review_date:
            raise serializers.ValidationError({"next_review_date": "The next review date must be after the last review date."})

        if generated_document:
            attrs.setdefault("module_key", generated_document.module_key)
            attrs.setdefault("module_label", generated_document.module_label)
            attrs.setdefault("record_id", generated_document.record_id)
            attrs.setdefault("record_title", generated_document.record_title)
            attrs.setdefault("current_version_label", generated_document.version_label)

        return attrs


class ReviewRecordSerializer(AuditFieldsSerializerMixin):
    review_cycle_title = serializers.CharField(source="review_cycle.title", read_only=True)
    generated_document_title = serializers.CharField(source="generated_document.title", read_only=True)

    class Meta:
        model = ReviewRecord
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["review_cycle", "generated_document"])

        review_cycle = attrs.get("review_cycle", getattr(self.instance, "review_cycle", None))
        generated_document = attrs.get("generated_document", getattr(self.instance, "generated_document", None))
        review_date = attrs.get("review_date", getattr(self.instance, "review_date", None))
        next_review_date = attrs.get("next_review_date", getattr(self.instance, "next_review_date", None))
        decision = attrs.get("decision", getattr(self.instance, "decision", None))
        errors = {}

        if review_cycle and not generated_document and review_cycle.generated_document_id:
            attrs["generated_document"] = review_cycle.generated_document
            generated_document = review_cycle.generated_document

        if review_date and next_review_date and next_review_date < review_date:
            errors["next_review_date"] = "The next review date must be after the review date."

        if decision == ReviewDecision.CHANGES_REQUESTED and not (attrs.get("recommendations") or getattr(self.instance, "recommendations", "")):
            errors["recommendations"] = "Add the requested changes before recording this decision."

        if generated_document and not attrs.get("version_label"):
            attrs["version_label"] = generated_document.version_label

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class ChangeLogEntrySerializer(AuditFieldsSerializerMixin):
    generated_document_title = serializers.CharField(source="generated_document.title", read_only=True)
    review_cycle_title = serializers.CharField(source="review_cycle.title", read_only=True)
    review_record_title = serializers.CharField(source="review_record.title", read_only=True)

    class Meta:
        model = ChangeLogEntry
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["generated_document", "review_cycle", "review_record"])
        return attrs


class GenerateReportDocumentSerializer(serializers.Serializer):
    module_key = serializers.CharField(max_length=80)
    module_label = serializers.CharField(max_length=120, required=False, allow_blank=True)
    report_preset = serializers.CharField(max_length=80, required=False, allow_blank=True)
    title = serializers.CharField(max_length=255, required=False, allow_blank=True)
    document_type = serializers.ChoiceField(
        choices=GeneratedDocument._meta.get_field("document_type").choices,
        default=GeneratedDocument._meta.get_field("document_type").default,
    )
    output_format = serializers.ChoiceField(
        choices=GeneratedDocument._meta.get_field("output_format").choices,
        default=GeneratedDocument._meta.get_field("output_format").default,
    )
    record_id = serializers.IntegerField(required=False, allow_null=True)
    record_title = serializers.CharField(max_length=255, required=False, allow_blank=True)
    search = serializers.CharField(max_length=255, required=False, allow_blank=True)
    rows = serializers.ListField(child=serializers.DictField(), allow_empty=False)
    columns = serializers.ListField(child=serializers.DictField(), required=False)


class TrainingProgramSerializer(AuditFieldsSerializerMixin):
    class Meta:
        model = TrainingProgram
        fields = "__all__"


class DeliverableMilestoneSerializer(AuditFieldsSerializerMixin):
    class Meta:
        model = DeliverableMilestone
        fields = "__all__"


class ActionPlanTaskSerializer(AuditFieldsSerializerMixin):
    related_risk_title = serializers.CharField(source="related_risk.title", read_only=True)
    related_milestone_title = serializers.CharField(source="related_milestone.title", read_only=True)
    related_infrastructure_name = serializers.CharField(source="related_infrastructure.name", read_only=True)

    class Meta:
        model = ActionPlanTask
        fields = "__all__"

    def validate(self, attrs):
        validate_same_organization(attrs, self.instance, ["related_risk", "related_milestone", "related_infrastructure"])
        return attrs
