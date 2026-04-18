from datetime import timedelta

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

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
    GeneratedDocument,
    GovernanceArtifact,
    Indicator,
    InformationShare,
    ChangeLogEntry,
    NonConformity,
    RiskAssessmentReview,
    RiskRegisterEntry,
    RiskScenario,
    ReviewCycle,
    ReviewRecord,
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
from .notifications import broadcast_notification
from .spatial import sync_point_geometry

STATUS_MESSAGES = {
    "draft": "moved to draft",
    "planned": "moved to planned",
    "in_progress": "is now in progress",
    "active": "is now active",
    "in_review": "entered review",
    "submitted": "submitted",
    "validated": "validated",
    "scheduled": "scheduled",
    "confirmed": "confirmed",
    "completed": "completed",
    "missed": "marked as missed",
    "rescheduled": "rescheduled",
    "identified": "was identified",
    "assessing": "entered assessment",
    "mitigating": "entered mitigation",
    "accepted": "was accepted",
    "closed": "was closed",
    "mapped": "was mapped",
    "reviewed": "was reviewed",
    "ready": "is now ready",
    "constrained": "is now constrained",
    "unavailable": "is now unavailable",
    "identified": "identified",
    "remediating": "entered remediation",
    "resolved": "resolved",
    "open": "opened",
    "rejected": "rejected",
    "expired": "expired",
    "reviewed": "reviewed",
    "analyzing": "entered analysis",
    "monitored": "is now monitored",
    "mitigated": "was mitigated",
    "validating": "entered validation",
    "prepared": "was prepared",
    "shared": "was shared",
    "received": "was received",
    "actioned": "was actioned",
    "declined": "was declined",
    "revoked": "was revoked",
    "generated": "was generated",
    "overdue": "is overdue",
    "superseded": "was superseded",
    "changes_requested": "needs changes",
}


@receiver(pre_save, sender=CriticalInfrastructure)
@receiver(pre_save, sender=EmergencyResponseAsset)
@receiver(pre_save, sender=AssetInventoryItem)
@receiver(pre_save, sender=ThreatEvent)
def sync_geometry_before_save(sender, instance, **kwargs):
    sync_point_geometry(instance)


def format_schedule_value(value):
    if not value:
        return ""
    if hasattr(value, "hour"):
        try:
            return timezone.localtime(value).strftime("%d %b %Y %H:%M")
        except Exception:
            return str(value)
    return str(value)


def snapshot_previous_state(sender, instance, tracked_fields):
    if not instance.pk:
        instance._previous_state = {}
        return

    instance._previous_state = sender.objects.filter(pk=instance.pk).values(*tracked_fields).first() or {}


def previous_value(instance, field_name):
    return getattr(instance, "_previous_state", {}).get(field_name)


def field_changed(instance, field_name, created):
    return created or previous_value(instance, field_name) != getattr(instance, field_name)


def format_choice_value(instance, field_name):
    display = getattr(instance, f"get_{field_name}_display", None)
    if callable(display):
        try:
            return str(display()).strip()
        except Exception:
            return ""
    value = getattr(instance, field_name, "")
    if isinstance(value, str):
        return value.replace("_", " ").strip().title()
    return str(value).strip()


def build_transition_message(instance, field_name):
    value = getattr(instance, field_name, "")
    explicit = STATUS_MESSAGES.get(value)
    if explicit:
        return explicit

    label = format_choice_value(instance, field_name).lower()
    if label:
        return f"moved to {label}"
    return f"updated {field_name.replace('_', ' ')}"


def notify_review_schedule(instance, created, label, status_field="status", terminal_values=None):
    if not getattr(instance, "next_review_date", None):
        return
    if terminal_values is None:
        terminal_values = {"completed", "archived"}
    if not field_changed(instance, "next_review_date", created) and not field_changed(instance, status_field, created):
        return
    if getattr(instance, status_field, "") in terminal_values:
        return

    broadcast_notification(f"{label} review scheduled: {instance.title} on {instance.next_review_date}", organization=getattr(instance, "organization", None))


def notify_due_date(instance, created, label, date_field="due_date", title_attr="title", status_field="status", terminal_values=None):
    due_date = getattr(instance, date_field, None)
    if not due_date:
        return
    if terminal_values is None:
        terminal_values = {"completed", "archived", "validated"}
    if not field_changed(instance, date_field, created) and not field_changed(instance, status_field, created):
        return
    if getattr(instance, status_field, "") in terminal_values:
        return

    title = getattr(instance, title_attr, "") or str(instance)
    broadcast_notification(f"{label} scheduled: {title} on {due_date}", organization=getattr(instance, "organization", None))


def notify_workflow_transition(instance, created, label, title_attr="title", field_name="status"):
    if not field_changed(instance, field_name, created):
        return

    message = build_transition_message(instance, field_name)
    if not message:
        return

    title = getattr(instance, title_attr, "") or str(instance)
    broadcast_notification(f"{label} {message}: {title}", organization=getattr(instance, "organization", None))


def create_change_log_entry(
    *,
    organization,
    title,
    change_type,
    summary="",
    generated_document=None,
    review_cycle=None,
    review_record=None,
    module_key="",
    module_label="",
    record_id=None,
    record_title="",
    version_label="",
    changed_by_name="",
    change_metadata=None,
):
    if not organization:
        return

    ChangeLogEntry.objects.create(
        organization=organization,
        generated_document=generated_document,
        review_cycle=review_cycle,
        review_record=review_record,
        title=title,
        module_key=module_key,
        module_label=module_label,
        record_id=record_id,
        record_title=record_title,
        change_type=change_type,
        version_label=version_label,
        summary=summary,
        change_metadata=change_metadata or {},
        changed_by_name=changed_by_name,
    )


def sync_review_outcomes(instance):
    review_cycle = instance.review_cycle
    generated_document = instance.generated_document

    if review_cycle:
        review_cycle.last_review_date = instance.review_date
        if instance.next_review_date:
            review_cycle.next_review_date = instance.next_review_date
        elif review_cycle.cadence_days and instance.review_date:
            review_cycle.next_review_date = instance.review_date + timedelta(days=review_cycle.cadence_days)
        review_cycle.current_version_label = instance.version_label or review_cycle.current_version_label or ""
        review_cycle.status = "completed" if instance.decision == "approved" and not review_cycle.next_review_date else "active"
        if review_cycle.next_review_date and review_cycle.next_review_date < timezone.localdate() and review_cycle.status not in {"completed", "archived"}:
            review_cycle.status = "overdue"
        review_cycle.save(update_fields=["last_review_date", "next_review_date", "current_version_label", "status", "updated_at"])

    if generated_document:
        update_fields = ["updated_at"]
        if instance.decision == "approved":
            generated_document.status = "approved"
            generated_document.published_on = timezone.now()
            generated_document.approved_by_name = instance.reviewer_name
            update_fields.extend(["status", "published_on", "approved_by_name"])
        elif instance.decision == "superseded":
            generated_document.status = "superseded"
            update_fields.append("status")
        else:
            generated_document.status = "in_review"
            update_fields.append("status")
        generated_document.save(update_fields=update_fields)


@receiver(pre_save, sender=Stakeholder)
def snapshot_stakeholder_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status"])


@receiver(pre_save, sender=RiskRegisterEntry)
def snapshot_risk_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["risk_level", "response_deadline", "treatment_status"])


@receiver(pre_save, sender=SimulationExercise)
def snapshot_exercise_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["planned_date", "status"])


@receiver(pre_save, sender=DeliverableMilestone)
def snapshot_deliverable_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["due_date", "status"])


@receiver(pre_save, sender=CriticalInfrastructure)
def snapshot_mapping_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["mapping_status", "designation_status"])


@receiver(pre_save, sender=GovernanceArtifact)
def snapshot_artifact_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "next_review_date"])


@receiver(pre_save, sender=DeskStudyReview)
def snapshot_desk_study_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "due_date"])


@receiver(pre_save, sender=StakeholderConsultation)
def snapshot_consultation_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "start_datetime", "next_follow_up_date", "meeting_link"])


@receiver(pre_save, sender=CapacityAssessment)
def snapshot_capacity_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "due_date", "gap_level"])


@receiver(pre_save, sender=AssetInventoryItem)
def snapshot_asset_inventory_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "criticality_level"])


@receiver(pre_save, sender=ThreatEvent)
def snapshot_threat_event_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "severity", "last_seen_at"])


@receiver(pre_save, sender=VulnerabilityRecord)
def snapshot_vulnerability_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "severity", "remediation_due_date"])


@receiver(pre_save, sender=RiskScenario)
def snapshot_risk_scenario_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "risk_level", "treatment_status", "review_due_date"])


@receiver(pre_save, sender=RiskAssessmentReview)
def snapshot_risk_review_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "decision", "follow_up_date"])


@receiver(pre_save, sender=ThreatBulletin)
def snapshot_threat_bulletin_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "severity", "issued_on", "valid_until"])


@receiver(pre_save, sender=Indicator)
def snapshot_indicator_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "last_seen_at"])


@receiver(pre_save, sender=DistributionGroup)
def snapshot_distribution_group_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status"])


@receiver(pre_save, sender=GeneratedDocument)
def snapshot_generated_document_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "published_on", "version_label"])


@receiver(pre_save, sender=ReviewCycle)
def snapshot_review_cycle_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "next_review_date", "current_version_label"])


@receiver(pre_save, sender=ReviewRecord)
def snapshot_review_record_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "decision", "next_review_date"])


@receiver(pre_save, sender=InformationShare)
def snapshot_information_share_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "shared_at", "acknowledgement_due_date"])


@receiver(pre_save, sender=Acknowledgement)
def snapshot_acknowledgement_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "responded_at"])


@receiver(pre_save, sender=ContingencyPlan)
def snapshot_plan_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "next_review_date"])


@receiver(pre_save, sender=CyberStandard)
def snapshot_standard_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "next_review_date"])


@receiver(pre_save, sender=AuditFramework)
def snapshot_audit_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "next_review_date"])


@receiver(pre_save, sender=StandardRequirement)
def snapshot_requirement_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status"])


@receiver(pre_save, sender=StandardControl)
def snapshot_control_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status"])


@receiver(pre_save, sender=ConformityAssessment)
def snapshot_conformity_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "conformity_level", "next_review_date"])


@receiver(pre_save, sender=ControlEvidence)
def snapshot_control_evidence_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "validity_until"])


@receiver(pre_save, sender=AuditPlan)
def snapshot_audit_plan_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "planned_start_date", "planned_end_date"])


@receiver(pre_save, sender=AuditChecklist)
def snapshot_audit_checklist_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "result"])


@receiver(pre_save, sender=AuditFinding)
def snapshot_audit_finding_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "severity", "due_date"])


@receiver(pre_save, sender=NonConformity)
def snapshot_non_conformity_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "severity", "due_date"])


@receiver(pre_save, sender=CorrectiveAction)
def snapshot_corrective_action_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "due_date", "blocker_summary"])


@receiver(pre_save, sender=EmergencyResponseAsset)
def snapshot_emergency_asset_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["availability_status"])


@receiver(pre_save, sender=TrainingProgram)
def snapshot_training_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status"])


@receiver(pre_save, sender=ActionPlanTask)
def snapshot_action_plan_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "due_date", "blocker_summary"])


@receiver(post_save, sender=Stakeholder)
def notify_stakeholder_activity(sender, instance, created, **kwargs):
    notify_workflow_transition(instance, created, "Stakeholder engagement", title_attr="name")


@receiver(post_save, sender=RiskRegisterEntry)
def notify_high_risk(sender, instance, created, **kwargs):
    if instance.risk_level not in {"high", "critical"}:
        return
    if not field_changed(instance, "risk_level", created) and not field_changed(instance, "response_deadline", created):
        return

    action = "registered" if created else "updated"
    broadcast_notification(f"{instance.get_risk_level_display()} risk {action}: {instance.title}", organization=getattr(instance, "organization", None))


@receiver(post_save, sender=RiskRegisterEntry)
def notify_risk_activity(sender, instance, created, **kwargs):
    notify_due_date(
        instance,
        created,
        "Risk response",
        date_field="response_deadline",
        status_field="treatment_status",
        terminal_values={"closed"},
    )
    notify_workflow_transition(instance, created, "Risk treatment", field_name="treatment_status")


@receiver(post_save, sender=SimulationExercise)
def notify_exercise_schedule(sender, instance, created, **kwargs):
    if instance.planned_date and instance.status in {"planned", "in_progress"} and (
        field_changed(instance, "planned_date", created) or field_changed(instance, "status", created)
    ):
        action = "scheduled" if created else "updated"
        broadcast_notification(f"Exercise {action}: {instance.title} on {instance.planned_date}", organization=getattr(instance, "organization", None))
    notify_workflow_transition(instance, created, "Simulation exercise")


@receiver(post_save, sender=DeliverableMilestone)
def notify_deliverable_deadline(sender, instance, created, **kwargs):
    if instance.due_date and instance.status not in {"completed", "validated", "archived"} and (
        field_changed(instance, "due_date", created) or field_changed(instance, "status", created)
    ):
        action = "tracked" if created else "updated"
        broadcast_notification(f"Deliverable {action}: {instance.title} due on {instance.due_date}", organization=getattr(instance, "organization", None))
    notify_workflow_transition(instance, created, "Deliverable milestone")


@receiver(post_save, sender=CriticalInfrastructure)
def notify_mapping_progress(sender, instance, created, **kwargs):
    notify_workflow_transition(instance, created, "Infrastructure mapping", title_attr="name", field_name="mapping_status")

    if instance.mapping_status in {"mapped", "reviewed"} and field_changed(instance, "mapping_status", created):
        broadcast_notification(f"Infrastructure mapping updated: {instance.name} is {instance.get_mapping_status_display().lower()}", organization=getattr(instance, "organization", None))

    if instance.designation_status in {"designated", "validated"} and field_changed(instance, "designation_status", created):
        broadcast_notification(f"Infrastructure designation updated: {instance.name} is {instance.get_designation_status_display().lower()}", organization=getattr(instance, "organization", None))


@receiver(post_save, sender=GovernanceArtifact)
def notify_artifact_activity(sender, instance, created, **kwargs):
    notify_review_schedule(instance, created, "Governance artifact")
    notify_workflow_transition(instance, created, "Governance artifact")


@receiver(post_save, sender=DeskStudyReview)
def notify_desk_study_activity(sender, instance, created, **kwargs):
    notify_due_date(instance, created, "Desk study review")
    notify_workflow_transition(instance, created, "Desk study review")


@receiver(post_save, sender=StakeholderConsultation)
def notify_consultation_activity(sender, instance, created, **kwargs):
    if instance.start_datetime and instance.status in {"scheduled", "confirmed", "rescheduled"} and (
        field_changed(instance, "start_datetime", created) or field_changed(instance, "status", created) or field_changed(instance, "meeting_link", created)
    ):
        channel = instance.get_engagement_channel_display().lower()
        broadcast_notification(
            f"Consultation meeting scheduled: {instance.title} on {format_schedule_value(instance.start_datetime)} via {channel}",
            organization=getattr(instance, "organization", None),
        )

    if instance.next_follow_up_date and (
        field_changed(instance, "next_follow_up_date", created) or field_changed(instance, "status", created)
    ) and instance.status not in {"completed", "missed", "archived"}:
        broadcast_notification(
            f"Consultation follow-up due: {instance.title} on {instance.next_follow_up_date}",
            organization=getattr(instance, "organization", None),
        )

    notify_workflow_transition(instance, created, "Consultation")


@receiver(post_save, sender=CapacityAssessment)
def notify_capacity_activity(sender, instance, created, **kwargs):
    notify_due_date(instance, created, "Capacity assessment")

    if instance.gap_level in {"high", "critical"} and field_changed(instance, "gap_level", created):
        broadcast_notification(f"Capacity gap identified: {instance.title} is {instance.get_gap_level_display().lower()}", organization=getattr(instance, "organization", None))

    notify_workflow_transition(instance, created, "Capacity assessment")


@receiver(post_save, sender=AssetInventoryItem)
def notify_asset_inventory_activity(sender, instance, created, **kwargs):
    notify_workflow_transition(instance, created, "Asset inventory item", title_attr="name")

    if instance.criticality_level in {"high", "critical"} and (
        field_changed(instance, "criticality_level", created) or field_changed(instance, "status", created)
    ):
        broadcast_notification(
            f"Critical asset inventory item flagged: {instance.name}",
            organization=getattr(instance, "organization", None),
        )


@receiver(post_save, sender=ThreatEvent)
def notify_threat_event_activity(sender, instance, created, **kwargs):
    notify_workflow_transition(instance, created, "Threat event")

    if instance.severity in {"high", "critical"} and (
        field_changed(instance, "severity", created) or field_changed(instance, "status", created)
    ):
        broadcast_notification(
            f"High-priority threat event detected: {instance.title}",
            organization=getattr(instance, "organization", None),
        )


@receiver(post_save, sender=VulnerabilityRecord)
def notify_vulnerability_activity(sender, instance, created, **kwargs):
    notify_due_date(
        instance,
        created,
        "Vulnerability remediation",
        date_field="remediation_due_date",
        status_field="status",
        terminal_values={"resolved", "closed"},
    )
    notify_workflow_transition(instance, created, "Vulnerability record")


@receiver(post_save, sender=RiskScenario)
def notify_risk_scenario_activity(sender, instance, created, **kwargs):
    notify_due_date(
        instance,
        created,
        "Risk scenario review",
        date_field="review_due_date",
        status_field="status",
        terminal_values={"completed", "archived"},
    )
    notify_workflow_transition(instance, created, "Risk scenario")
    notify_workflow_transition(instance, created, "Risk scenario treatment", field_name="treatment_status")

    if instance.risk_level in {"high", "critical"} and (
        field_changed(instance, "risk_level", created) or field_changed(instance, "treatment_status", created)
    ):
        broadcast_notification(
            f"High-priority risk scenario logged: {instance.title}",
            organization=getattr(instance, "organization", None),
        )


@receiver(post_save, sender=RiskAssessmentReview)
def notify_risk_review_activity(sender, instance, created, **kwargs):
    notify_due_date(
        instance,
        created,
        "Risk assessment follow-up",
        date_field="follow_up_date",
        status_field="status",
        terminal_values={"completed", "archived"},
    )
    notify_workflow_transition(instance, created, "Risk assessment review")

    if field_changed(instance, "decision", created):
        broadcast_notification(
            f"Risk review decision recorded: {instance.title} set to {instance.get_decision_display().lower()}",
            organization=getattr(instance, "organization", None),
        )


@receiver(post_save, sender=ThreatBulletin)
def notify_threat_bulletin_activity(sender, instance, created, **kwargs):
    if instance.issued_on and (
        field_changed(instance, "issued_on", created) or field_changed(instance, "status", created)
    ) and instance.status not in {"archived"}:
        broadcast_notification(
            f"Threat bulletin issued: {instance.title} on {instance.issued_on}",
            organization=getattr(instance, "organization", None),
        )

    notify_due_date(
        instance,
        created,
        "Threat bulletin validity",
        date_field="valid_until",
        status_field="status",
        terminal_values={"archived"},
    )
    notify_workflow_transition(instance, created, "Threat bulletin")


@receiver(post_save, sender=Indicator)
def notify_indicator_activity(sender, instance, created, **kwargs):
    notify_workflow_transition(instance, created, "Threat indicator")


@receiver(post_save, sender=DistributionGroup)
def notify_distribution_group_activity(sender, instance, created, **kwargs):
    notify_workflow_transition(instance, created, "Distribution group", title_attr="title")


@receiver(post_save, sender=InformationShare)
def notify_information_share_activity(sender, instance, created, **kwargs):
    if instance.shared_at and (
        field_changed(instance, "shared_at", created) or field_changed(instance, "status", created)
    ) and instance.status in {"shared", "acknowledged", "closed"}:
        broadcast_notification(
            f"Information share released: {instance.title}",
            organization=getattr(instance, "organization", None),
        )

    notify_due_date(
        instance,
        created,
        "Information share acknowledgement",
        date_field="acknowledgement_due_date",
        status_field="status",
        terminal_values={"closed"},
    )
    notify_workflow_transition(instance, created, "Information share")


@receiver(post_save, sender=Acknowledgement)
def notify_acknowledgement_activity(sender, instance, created, **kwargs):
    notify_workflow_transition(instance, created, "Information acknowledgement", title_attr="action_note")


@receiver(post_save, sender=GeneratedDocument)
def notify_generated_document_activity(sender, instance, created, **kwargs):
    if created:
        broadcast_notification(
            f"Generated document ready: {instance.title} ({instance.version_label})",
            organization=getattr(instance, "organization", None),
        )
        create_change_log_entry(
            organization=instance.organization,
            generated_document=instance,
            title=instance.title,
            change_type="generated",
            summary=f"Generated {instance.get_document_type_display().lower()} {instance.version_label}.",
            module_key=instance.module_key,
            module_label=instance.module_label,
            record_id=instance.record_id,
            record_title=instance.record_title,
            version_label=instance.version_label,
            changed_by_name=instance.generated_by_name,
        )
        return

    notify_workflow_transition(instance, created, "Generated document")

    if field_changed(instance, "status", created):
        change_type = {
            "approved": "approved",
            "superseded": "superseded",
            "archived": "archived",
        }.get(instance.status, "updated")
        create_change_log_entry(
            organization=instance.organization,
            generated_document=instance,
            title=instance.title,
            change_type=change_type,
            summary=f"Document moved to {instance.get_status_display().lower()}.",
            module_key=instance.module_key,
            module_label=instance.module_label,
            record_id=instance.record_id,
            record_title=instance.record_title,
            version_label=instance.version_label,
            changed_by_name=instance.approved_by_name or instance.generated_by_name,
        )


@receiver(post_save, sender=ReviewCycle)
def notify_review_cycle_activity(sender, instance, created, **kwargs):
    notify_due_date(
        instance,
        created,
        "Review cycle",
        date_field="next_review_date",
        status_field="status",
        terminal_values={"completed", "archived"},
    )
    notify_workflow_transition(instance, created, "Review cycle")

    if created or field_changed(instance, "next_review_date", created) or field_changed(instance, "status", created):
        create_change_log_entry(
            organization=instance.organization,
            review_cycle=instance,
            generated_document=instance.generated_document,
            title=instance.title,
            change_type="updated",
            summary=(
                f"Review cycle updated with next review on {instance.next_review_date}."
                if instance.next_review_date
                else "Review cycle updated."
            ),
            module_key=instance.module_key,
            module_label=instance.module_label,
            record_id=instance.record_id,
            record_title=instance.record_title,
            version_label=instance.current_version_label,
            changed_by_name=instance.owner_name,
        )


@receiver(post_save, sender=ReviewRecord)
def notify_review_record_activity(sender, instance, created, **kwargs):
    sync_review_outcomes(instance)

    if created or field_changed(instance, "decision", created):
        broadcast_notification(
            f"Review recorded: {instance.title} marked as {instance.get_decision_display().lower()}",
            organization=getattr(instance, "organization", None),
        )

    notify_due_date(
        instance,
        created,
        "Review follow-up",
        date_field="next_review_date",
        status_field="status",
        terminal_values={"completed", "archived"},
    )
    notify_workflow_transition(instance, created, "Review record")

    if created or field_changed(instance, "decision", created) or field_changed(instance, "status", created):
        create_change_log_entry(
            organization=instance.organization,
            generated_document=instance.generated_document,
            review_cycle=instance.review_cycle,
            review_record=instance,
            title=instance.title,
            change_type="review_recorded" if instance.decision not in {"approved", "superseded"} else instance.decision,
            summary=f"Review decision recorded as {instance.get_decision_display().lower()}.",
            module_key=getattr(instance.review_cycle, "module_key", "") or getattr(instance.generated_document, "module_key", ""),
            module_label=getattr(instance.review_cycle, "module_label", "") or getattr(instance.generated_document, "module_label", ""),
            record_id=getattr(instance.review_cycle, "record_id", None) or getattr(instance.generated_document, "record_id", None),
            record_title=getattr(instance.review_cycle, "record_title", "") or getattr(instance.generated_document, "record_title", ""),
            version_label=instance.version_label,
            changed_by_name=instance.reviewer_name,
        )


@receiver(post_save, sender=ContingencyPlan)
def notify_plan_activity(sender, instance, created, **kwargs):
    notify_review_schedule(instance, created, "Contingency plan")
    notify_workflow_transition(instance, created, "Contingency plan")


@receiver(post_save, sender=EmergencyResponseAsset)
def notify_emergency_asset_activity(sender, instance, created, **kwargs):
    notify_workflow_transition(instance, created, "Emergency response asset", title_attr="name", field_name="availability_status")


@receiver(post_save, sender=CyberStandard)
def notify_standard_activity(sender, instance, created, **kwargs):
    notify_review_schedule(instance, created, "Cyber standard")
    notify_workflow_transition(instance, created, "Cyber standard")


@receiver(post_save, sender=AuditFramework)
def notify_audit_activity(sender, instance, created, **kwargs):
    notify_review_schedule(instance, created, "Audit framework")
    notify_workflow_transition(instance, created, "Audit framework")


@receiver(post_save, sender=StandardRequirement)
def notify_requirement_activity(sender, instance, created, **kwargs):
    notify_workflow_transition(instance, created, "Standard requirement")


@receiver(post_save, sender=StandardControl)
def notify_control_activity(sender, instance, created, **kwargs):
    notify_workflow_transition(instance, created, "Standard control")


@receiver(post_save, sender=ConformityAssessment)
def notify_conformity_activity(sender, instance, created, **kwargs):
    notify_review_schedule(instance, created, "Conformity assessment")
    notify_workflow_transition(instance, created, "Conformity assessment")

    if instance.conformity_level == "non_conformant" and (
        field_changed(instance, "conformity_level", created) or field_changed(instance, "status", created)
    ):
        broadcast_notification(
            f"Non-conformant assessment flagged: {instance.title}",
            organization=getattr(instance, "organization", None),
        )


@receiver(post_save, sender=ControlEvidence)
def notify_control_evidence_activity(sender, instance, created, **kwargs):
    if instance.validity_until and field_changed(instance, "validity_until", created):
        broadcast_notification(
            f"Evidence validity updated: {instance.title} valid until {instance.validity_until}",
            organization=getattr(instance, "organization", None),
        )
    notify_workflow_transition(instance, created, "Control evidence")


@receiver(post_save, sender=AuditPlan)
def notify_audit_plan_activity(sender, instance, created, **kwargs):
    if instance.planned_start_date and (
        field_changed(instance, "planned_start_date", created) or field_changed(instance, "status", created)
    ) and instance.status not in {"completed", "archived"}:
        broadcast_notification(
            f"Audit plan scheduled: {instance.title} starts on {instance.planned_start_date}",
            organization=getattr(instance, "organization", None),
        )
    notify_workflow_transition(instance, created, "Audit plan")


@receiver(post_save, sender=AuditChecklist)
def notify_audit_checklist_activity(sender, instance, created, **kwargs):
    notify_workflow_transition(instance, created, "Audit checklist item")


@receiver(post_save, sender=AuditFinding)
def notify_audit_finding_activity(sender, instance, created, **kwargs):
    notify_due_date(
        instance,
        created,
        "Audit finding",
        status_field="status",
        terminal_values={"resolved", "closed"},
    )
    notify_workflow_transition(instance, created, "Audit finding")

    if instance.severity in {"high", "critical"} and (
        field_changed(instance, "severity", created) or field_changed(instance, "status", created)
    ):
        broadcast_notification(
            f"High-severity audit finding: {instance.title}",
            organization=getattr(instance, "organization", None),
        )


@receiver(post_save, sender=NonConformity)
def notify_non_conformity_activity(sender, instance, created, **kwargs):
    notify_due_date(
        instance,
        created,
        "Non-conformity",
        status_field="status",
        terminal_values={"resolved", "closed"},
    )
    notify_workflow_transition(instance, created, "Non-conformity")


@receiver(post_save, sender=CorrectiveAction)
def notify_corrective_action_activity(sender, instance, created, **kwargs):
    notify_due_date(instance, created, "Corrective action")

    if instance.blocker_summary and (
        field_changed(instance, "blocker_summary", created) or field_changed(instance, "status", created)
    ) and instance.status not in {"completed", "archived"}:
        broadcast_notification(
            f"Corrective action blocker flagged: {instance.title}",
            organization=getattr(instance, "organization", None),
        )

    notify_workflow_transition(instance, created, "Corrective action")


@receiver(post_save, sender=TrainingProgram)
def notify_training_activity(sender, instance, created, **kwargs):
    notify_workflow_transition(instance, created, "Training program")


@receiver(post_save, sender=ActionPlanTask)
def notify_action_plan_activity(sender, instance, created, **kwargs):
    notify_due_date(instance, created, "Action plan task")

    if instance.blocker_summary and (
        field_changed(instance, "blocker_summary", created) or field_changed(instance, "status", created)
    ) and instance.status not in {"completed", "archived"}:
        broadcast_notification(f"Action plan blocker flagged: {instance.title}", organization=getattr(instance, "organization", None))

    notify_workflow_transition(instance, created, "Action plan task")
