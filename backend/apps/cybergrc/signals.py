from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

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
    SimulationExercise,
    Stakeholder,
    StakeholderConsultation,
    TrainingProgram,
)
from .notifications import broadcast_notification

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
}


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

    title = getattr(instance, title_attr, str(instance))
    broadcast_notification(f"{label} scheduled: {title} on {due_date}", organization=getattr(instance, "organization", None))


def notify_workflow_transition(instance, created, label, title_attr="title", field_name="status"):
    if not field_changed(instance, field_name, created):
        return

    message = build_transition_message(instance, field_name)
    if not message:
        return

    title = getattr(instance, title_attr, str(instance))
    broadcast_notification(f"{label} {message}: {title}", organization=getattr(instance, "organization", None))


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


@receiver(pre_save, sender=ContingencyPlan)
def snapshot_plan_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "next_review_date"])


@receiver(pre_save, sender=CyberStandard)
def snapshot_standard_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "next_review_date"])


@receiver(pre_save, sender=AuditFramework)
def snapshot_audit_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "next_review_date"])


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
