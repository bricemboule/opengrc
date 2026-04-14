from rest_framework import serializers

from apps.core.serializers import AuditFieldsSerializerMixin

from .models import (
    ActionPlanTask,
    AuditFramework,
    CapacityAssessment,
    ContingencyPlan,
    CriticalInfrastructure,
    CyberStandard,
    DeliverableMilestone,
    DeskStudyReview,
    EmergencyResponseAsset,
    GovernanceArtifact,
    RiskRegisterEntry,
    Sector,
    SimulationExercise,
    Stakeholder,
    StakeholderConsultation,
    TrainingProgram,
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


def apply_relation_name_fallback(attrs, instance, relation_name, target_field_name, source_attribute="name"):
    related = attrs.get(relation_name, getattr(instance, relation_name, None))
    if related:
        attrs[target_field_name] = getattr(related, source_attribute, "") or ""
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
