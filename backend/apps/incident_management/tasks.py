from datetime import timedelta

from django.utils import timezone

from apps.communications.notifications import dispatch_notification

from .models import AssetAllocation, Incident, IncidentTask, SOPExecution


def send_incident_reminders():
    now = timezone.now()
    reminder_window = now + timedelta(hours=6)
    task_window = now + timedelta(hours=24)

    due_updates = Incident.objects.filter(
        is_deleted=False,
        status__in=["reported", "assessing", "active", "contained", "recovering"],
        next_update_due__isnull=False,
        next_update_due__lte=reminder_window,
    ).select_related("organization")

    for incident in due_updates:
        dispatch_notification(
            title="Incident update due",
            message=f"{incident.title} needs an operational update before {incident.next_update_due:%b %d, %Y %H:%M}.",
            organization=incident.organization,
            source="incident_management",
            send_email=incident.severity in {"critical", "national"},
        )

    due_tasks = IncidentTask.objects.filter(
        is_deleted=False,
        status__in=["planned", "in_progress", "blocked"],
        due_at__isnull=False,
        due_at__lte=task_window,
    ).select_related("organization", "incident")

    for task in due_tasks:
        dispatch_notification(
            title="Incident task due soon",
            message=f"{task.title} linked to {task.incident.title} is due before {task.due_at:%b %d, %Y %H:%M}.",
            organization=task.organization,
            source="incident_management",
            send_email=False,
        )

    due_executions = SOPExecution.objects.filter(
        is_deleted=False,
        status__in=["planned", "active", "blocked"],
        target_completion_at__isnull=False,
        target_completion_at__lte=task_window,
    ).select_related("organization", "incident")

    for execution in due_executions:
        dispatch_notification(
            title="SOP execution due soon",
            message=f"{execution.title} for {execution.incident.title} should complete before {execution.target_completion_at:%b %d, %Y %H:%M}.",
            organization=execution.organization,
            source="incident_management",
            send_email=execution.incident.severity in {"critical", "national"},
        )

    pending_allocations = AssetAllocation.objects.filter(
        is_deleted=False,
        status__in=["requested", "approved", "mobilizing"],
        requested_at__lte=now - timedelta(hours=1),
    ).select_related("organization", "incident", "emergency_asset")

    for allocation in pending_allocations:
        dispatch_notification(
            title="Emergency asset allocation pending",
            message=f"{allocation.emergency_asset.name} for {allocation.incident.title} is still {allocation.get_status_display().lower()}.",
            organization=allocation.organization,
            source="incident_management",
            send_email=False,
        )
