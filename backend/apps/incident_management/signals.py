from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.communications.notifications import dispatch_notification

from .models import AssetAllocation, Incident, IncidentAssignment, IncidentTask, SOPExecution, SOPExecutionStep


@receiver(post_save, sender=Incident)
def notify_incident_created(sender, instance, created, **kwargs):
    if not created:
        return

    title = "New incident reported"
    if instance.severity in {"critical", "national"}:
        title = "Critical incident reported"

    dispatch_notification(
        title=title,
        message=f"{instance.title} is now tracked with {instance.get_severity_display().lower()} severity and {instance.get_status_display().lower()} status.",
        organization=instance.organization,
        source="incident_management",
        send_email=instance.severity in {"critical", "national"},
    )


@receiver(post_save, sender=IncidentTask)
def notify_blocked_incident_task(sender, instance, created, **kwargs):
    if not instance.organization_id:
        return
    if instance.status != "blocked" and not instance.blocker_summary:
        return

    dispatch_notification(
        title="Incident task blocked",
        message=f"{instance.title} for {instance.incident.title} is blocked and needs coordination attention.",
        organization=instance.organization,
        source="incident_management",
        send_email=False,
    )


@receiver(post_save, sender=IncidentAssignment)
def notify_incident_assignment(sender, instance, created, **kwargs):
    if not created or not instance.organization_id:
        return

    target_name = instance.assignee.full_name if instance.assignee and instance.assignee.full_name else getattr(instance.assignee, "email", "") or getattr(instance.stakeholder, "name", "")
    dispatch_notification(
        title="Incident role assigned",
        message=f"{target_name or 'A response actor'} was assigned as {instance.role_in_response} for {instance.incident.title}.",
        organization=instance.organization,
        source="incident_management",
        send_email=False,
    )


@receiver(post_save, sender=SOPExecution)
def notify_sop_execution_created(sender, instance, created, **kwargs):
    if not created or not instance.organization_id:
        return

    dispatch_notification(
        title="SOP execution launched",
        message=f"{instance.title} was created for {instance.incident.title} and is ready for operational execution.",
        organization=instance.organization,
        source="incident_management",
        send_email=instance.incident.severity in {"critical", "national"},
    )


@receiver(post_save, sender=SOPExecutionStep)
def notify_blocked_sop_execution_step(sender, instance, created, **kwargs):
    if not instance.organization_id:
        return
    if instance.status != "blocked" and not instance.blocker_summary:
        return

    dispatch_notification(
        title="SOP step blocked",
        message=f"{instance.title} in {instance.execution.title} is blocked and needs coordination support.",
        organization=instance.organization,
        source="incident_management",
        send_email=False,
    )


@receiver(post_save, sender=AssetAllocation)
def notify_asset_allocation(sender, instance, created, **kwargs):
    if not instance.organization_id:
        return

    if created:
        dispatch_notification(
            title="Emergency asset requested",
            message=f"{instance.emergency_asset.name} was requested for {instance.incident.title}.",
            organization=instance.organization,
            source="incident_management",
            send_email=False,
        )
        return

    if instance.status == "deployed":
        dispatch_notification(
            title="Emergency asset deployed",
            message=f"{instance.emergency_asset.name} is now deployed for {instance.incident.title}.",
            organization=instance.organization,
            source="incident_management",
            send_email=instance.incident.severity in {"critical", "national"},
        )
    elif instance.status == "released":
        dispatch_notification(
            title="Emergency asset released",
            message=f"{instance.emergency_asset.name} was released from {instance.incident.title}.",
            organization=instance.organization,
            source="incident_management",
            send_email=False,
        )
