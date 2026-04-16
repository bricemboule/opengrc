from datetime import timedelta

from celery import shared_task
from django.db.models import F, Q
from django.utils import timezone

from apps.communications.notifications import dispatch_notification

from .models import StakeholderConsultation

MEETING_ACTIVE_STATUSES = ("scheduled", "confirmed", "rescheduled")
MEETING_CLOSED_STATUSES = ("completed", "missed", "archived")


def format_meeting_time(value):
    try:
        return timezone.localtime(value).strftime("%d %b %Y %H:%M")
    except Exception:  # pragma: no cover - runtime guard
        return str(value)


@shared_task
def send_consultation_reminders():
    now = timezone.now()
    today = timezone.localdate()
    schedule_horizon = now + timedelta(hours=24)
    follow_up_horizon = today + timedelta(days=1)

    meeting_queryset = (
        StakeholderConsultation.objects.select_related("organization", "stakeholder")
        .filter(
            start_datetime__isnull=False,
            start_datetime__gte=now,
            start_datetime__lte=schedule_horizon,
            status__in=MEETING_ACTIVE_STATUSES,
        )
        .filter(Q(start_reminder_sent_for__isnull=True) | ~Q(start_reminder_sent_for=F("start_datetime")))
        .order_by("start_datetime", "id")
    )

    follow_up_queryset = (
        StakeholderConsultation.objects.select_related("organization", "stakeholder")
        .filter(
            next_follow_up_date__isnull=False,
            next_follow_up_date__gte=today,
            next_follow_up_date__lte=follow_up_horizon,
        )
        .exclude(status__in=MEETING_CLOSED_STATUSES)
        .filter(Q(follow_up_reminder_sent_for__isnull=True) | ~Q(follow_up_reminder_sent_for=F("next_follow_up_date")))
        .order_by("next_follow_up_date", "id")
    )

    meeting_notifications = 0
    follow_up_notifications = 0

    for consultation in meeting_queryset:
        stakeholder_name = consultation.stakeholder.name if consultation.stakeholder else "the target stakeholder"
        access_note = consultation.meeting_link or consultation.dial_in_details or consultation.meeting_location or "Open the consultation file for access details."
        dispatch_notification(
            title="Consultation meeting reminder",
            message=(
                f"{consultation.title} with {stakeholder_name} starts at {format_meeting_time(consultation.start_datetime)} "
                f"via {consultation.get_engagement_channel_display().lower()}. {access_note}"
            ),
            organization=consultation.organization,
            source="consultation_meeting_reminder",
            send_email=True,
        )
        consultation.start_reminder_sent_for = consultation.start_datetime
        consultation.save(update_fields=["start_reminder_sent_for", "updated_at"])
        meeting_notifications += 1

    for consultation in follow_up_queryset:
        stakeholder_name = consultation.stakeholder.name if consultation.stakeholder else "the relevant stakeholder"
        action_note = consultation.follow_up_actions or "Review the meeting notes and update the next action."
        dispatch_notification(
            title="Consultation follow-up reminder",
            message=f"Follow up {consultation.title} with {stakeholder_name} by {consultation.next_follow_up_date}. {action_note}",
            organization=consultation.organization,
            source="consultation_follow_up_reminder",
            send_email=True,
        )
        consultation.follow_up_reminder_sent_for = consultation.next_follow_up_date
        consultation.save(update_fields=["follow_up_reminder_sent_for", "updated_at"])
        follow_up_notifications += 1

    return {
        "meeting_notifications": meeting_notifications,
        "follow_up_notifications": follow_up_notifications,
    }
