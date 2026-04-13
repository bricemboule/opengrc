from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import (
    ActionPlanTask,
    AuditFramework,
    CapacityAssessment,
    ContingencyPlan,
    CriticalInfrastructure,
    CyberStandard,
    DeliverableMilestone,
    DeskStudyReview,
    GovernanceArtifact,
    RiskRegisterEntry,
    SimulationExercise,
    StakeholderConsultation,
    TrainingProgram,
)
from .notifications import broadcast_notification

STATUS_MESSAGES = {
    "in_review": "entered review",
    "submitted": "submitted",
    "validated": "validated",
    "completed": "completed",
}


def snapshot_previous_state(sender, instance, tracked_fields):
    if not instance.pk:
        instance._previous_state = {}
        return

    instance._previous_state = sender.objects.filter(pk=instance.pk).values(*tracked_fields).first() or {}


def previous_value(instance, field_name):
    return getattr(instance, "_previous_state", {}).get(field_name)


def field_changed(instance, field_name, created):
    return created or previous_value(instance, field_name) != getattr(instance, field_name)


def notify_review_schedule(instance, created, label):
    if not getattr(instance, "next_review_date", None):
        return
    if not field_changed(instance, "next_review_date", created) and not field_changed(instance, "status", created):
        return
    if getattr(instance, "status", "") in {"completed", "archived"}:
        return

    broadcast_notification(f"{label} review scheduled: {instance.title} on {instance.next_review_date}")


def notify_due_date(instance, created, label, date_field="due_date", title_attr="title"):
    due_date = getattr(instance, date_field, None)
    if not due_date:
        return
    if not field_changed(instance, date_field, created) and not field_changed(instance, "status", created):
        return
    if getattr(instance, "status", "") in {"completed", "archived", "validated"}:
        return

    title = getattr(instance, title_attr, str(instance))
    broadcast_notification(f"{label} scheduled: {title} on {due_date}")


def notify_workflow_transition(instance, created, label, title_attr="title"):
    if not field_changed(instance, "status", created):
        return

    message = STATUS_MESSAGES.get(getattr(instance, "status", ""))
    if not message:
        return

    title = getattr(instance, title_attr, str(instance))
    broadcast_notification(f"{label} {message}: {title}")


@receiver(pre_save, sender=RiskRegisterEntry)
def snapshot_risk_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["risk_level", "response_deadline"])


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
    snapshot_previous_state(sender, instance, ["status", "planned_date", "next_follow_up_date"])


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


@receiver(pre_save, sender=TrainingProgram)
def snapshot_training_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status"])


@receiver(pre_save, sender=ActionPlanTask)
def snapshot_action_plan_state(sender, instance, **kwargs):
    snapshot_previous_state(sender, instance, ["status", "due_date", "blocker_summary"])


@receiver(post_save, sender=RiskRegisterEntry)
def notify_high_risk(sender, instance, created, **kwargs):
    if instance.risk_level not in {"high", "critical"}:
        return
    if not field_changed(instance, "risk_level", created) and not field_changed(instance, "response_deadline", created):
        return

    action = "registered" if created else "updated"
    broadcast_notification(f"{instance.get_risk_level_display()} risk {action}: {instance.title}")


@receiver(post_save, sender=SimulationExercise)
def notify_exercise_schedule(sender, instance, created, **kwargs):
    if not instance.planned_date:
        return
    if instance.status not in {"planned", "in_progress"}:
        return
    if not field_changed(instance, "planned_date", created) and not field_changed(instance, "status", created):
        return

    action = "scheduled" if created else "updated"
    broadcast_notification(f"Exercise {action}: {instance.title} on {instance.planned_date}")


@receiver(post_save, sender=DeliverableMilestone)
def notify_deliverable_deadline(sender, instance, created, **kwargs):
    if not instance.due_date:
        return
    if instance.status in {"completed", "validated", "archived"}:
        return
    if not field_changed(instance, "due_date", created) and not field_changed(instance, "status", created):
        return

    action = "tracked" if created else "updated"
    broadcast_notification(f"Deliverable {action}: {instance.title} due on {instance.due_date}")


@receiver(post_save, sender=CriticalInfrastructure)
def notify_mapping_progress(sender, instance, created, **kwargs):
    if instance.mapping_status in {"mapped", "reviewed"} and field_changed(instance, "mapping_status", created):
        broadcast_notification(f"Infrastructure mapping updated: {instance.name} is {instance.get_mapping_status_display().lower()}")

    if instance.designation_status in {"designated", "validated"} and field_changed(instance, "designation_status", created):
        broadcast_notification(f"Infrastructure designation updated: {instance.name} is {instance.get_designation_status_display().lower()}")


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
    if instance.planned_date and instance.status in {"planned", "in_progress", "active"} and (
        field_changed(instance, "planned_date", created) or field_changed(instance, "status", created)
    ):
        broadcast_notification(f"Consultation scheduled: {instance.title} on {instance.planned_date}")

    if instance.next_follow_up_date and (
        field_changed(instance, "next_follow_up_date", created) or field_changed(instance, "status", created)
    ) and instance.status not in {"completed", "archived"}:
        broadcast_notification(f"Consultation follow-up due: {instance.title} on {instance.next_follow_up_date}")

    notify_workflow_transition(instance, created, "Consultation")


@receiver(post_save, sender=CapacityAssessment)
def notify_capacity_activity(sender, instance, created, **kwargs):
    notify_due_date(instance, created, "Capacity assessment")

    if instance.gap_level in {"high", "critical"} and field_changed(instance, "gap_level", created):
        broadcast_notification(f"Capacity gap identified: {instance.title} is {instance.get_gap_level_display().lower()}")

    notify_workflow_transition(instance, created, "Capacity assessment")


@receiver(post_save, sender=ContingencyPlan)
def notify_plan_activity(sender, instance, created, **kwargs):
    notify_review_schedule(instance, created, "Contingency plan")
    notify_workflow_transition(instance, created, "Contingency plan")


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
        broadcast_notification(f"Action plan blocker flagged: {instance.title}")

    notify_workflow_transition(instance, created, "Action plan task")