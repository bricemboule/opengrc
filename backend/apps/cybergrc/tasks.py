from datetime import timedelta

from celery import shared_task
from django.db.models import F, Q
from django.utils import timezone

from apps.communications.notifications import dispatch_notification

from .models import (
    AuditFinding,
    AuditPlan,
    ConformityAssessment,
    CorrectiveAction,
    GeneratedDocument,
    InformationShare,
    RiskAssessmentReview,
    RiskScenario,
    ReviewCycle,
    StakeholderConsultation,
    ThreatBulletin,
)

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


@shared_task
def send_compliance_reminders():
    today = timezone.localdate()
    review_horizon = today + timedelta(days=7)

    assessment_queryset = (
        ConformityAssessment.objects.select_related("organization")
        .filter(next_review_date__isnull=False, next_review_date__gte=today, next_review_date__lte=review_horizon)
        .exclude(status__in=("completed", "archived"))
        .order_by("next_review_date", "id")
    )

    audit_plan_queryset = (
        AuditPlan.objects.select_related("organization")
        .filter(planned_start_date__isnull=False, planned_start_date__gte=today, planned_start_date__lte=review_horizon)
        .exclude(status__in=("completed", "archived"))
        .order_by("planned_start_date", "id")
    )

    finding_queryset = (
        AuditFinding.objects.select_related("organization")
        .filter(due_date__isnull=False, due_date__gte=today, due_date__lte=review_horizon)
        .exclude(status__in=("resolved", "closed"))
        .order_by("due_date", "id")
    )

    corrective_action_queryset = (
        CorrectiveAction.objects.select_related("organization")
        .filter(due_date__isnull=False, due_date__gte=today, due_date__lte=review_horizon)
        .exclude(status__in=("completed", "archived"))
        .order_by("due_date", "id")
    )

    notifications_sent = 0

    for assessment in assessment_queryset:
        dispatch_notification(
            title="Conformity review due",
            message=f"{assessment.title} should be reviewed by {assessment.next_review_date}.",
            organization=assessment.organization,
            source="conformity_assessment_reminder",
            send_email=True,
        )
        notifications_sent += 1

    for audit_plan in audit_plan_queryset:
        dispatch_notification(
            title="Audit plan starting soon",
            message=f"{audit_plan.title} is scheduled to start on {audit_plan.planned_start_date}.",
            organization=audit_plan.organization,
            source="audit_plan_reminder",
            send_email=True,
        )
        notifications_sent += 1

    for finding in finding_queryset:
        dispatch_notification(
            title="Audit finding due",
            message=f"{finding.title} is due by {finding.due_date}.",
            organization=finding.organization,
            source="audit_finding_reminder",
            send_email=True,
        )
        notifications_sent += 1

    for corrective_action in corrective_action_queryset:
        dispatch_notification(
            title="Corrective action due",
            message=f"{corrective_action.title} is due by {corrective_action.due_date}.",
            organization=corrective_action.organization,
            source="corrective_action_reminder",
            send_email=True,
        )
        notifications_sent += 1

    return {"notifications_sent": notifications_sent}


@shared_task
def send_threat_and_risk_reminders():
    today = timezone.localdate()
    near_horizon = today + timedelta(days=3)
    review_horizon = today + timedelta(days=7)

    bulletin_queryset = (
        ThreatBulletin.objects.select_related("organization")
        .filter(valid_until__isnull=False, valid_until__gte=today, valid_until__lte=near_horizon)
        .exclude(status__in=("archived",))
        .order_by("valid_until", "id")
    )

    information_share_queryset = (
        InformationShare.objects.select_related("organization")
        .filter(acknowledgement_due_date__isnull=False, acknowledgement_due_date__gte=today, acknowledgement_due_date__lte=near_horizon)
        .exclude(status__in=("closed",))
        .order_by("acknowledgement_due_date", "id")
    )

    risk_scenario_queryset = (
        RiskScenario.objects.select_related("organization")
        .filter(review_due_date__isnull=False, review_due_date__gte=today, review_due_date__lte=review_horizon)
        .exclude(status__in=("completed", "archived"))
        .order_by("review_due_date", "id")
    )

    risk_review_queryset = (
        RiskAssessmentReview.objects.select_related("organization")
        .filter(follow_up_date__isnull=False, follow_up_date__gte=today, follow_up_date__lte=review_horizon)
        .exclude(status__in=("completed", "archived"))
        .order_by("follow_up_date", "id")
    )

    notifications_sent = 0

    for bulletin in bulletin_queryset:
        dispatch_notification(
            title="Threat bulletin validity ending soon",
            message=f"{bulletin.title} remains valid until {bulletin.valid_until}. Review whether it should be refreshed or archived.",
            organization=bulletin.organization,
            source="threat_bulletin_reminder",
            send_email=True,
        )
        notifications_sent += 1

    for information_share in information_share_queryset:
        dispatch_notification(
            title="Acknowledgement follow-up due",
            message=f"{information_share.title} needs acknowledgement by {information_share.acknowledgement_due_date}.",
            organization=information_share.organization,
            source="information_share_reminder",
            send_email=True,
        )
        notifications_sent += 1

    for scenario in risk_scenario_queryset:
        dispatch_notification(
            title="Risk scenario review due",
            message=f"{scenario.title} should be reviewed by {scenario.review_due_date}.",
            organization=scenario.organization,
            source="risk_scenario_review_reminder",
            send_email=True,
        )
        notifications_sent += 1

    for review in risk_review_queryset:
        dispatch_notification(
            title="Risk assessment follow-up due",
            message=f"{review.title} has a follow-up due by {review.follow_up_date}.",
            organization=review.organization,
            source="risk_assessment_follow_up_reminder",
            send_email=True,
        )
        notifications_sent += 1

    return {"notifications_sent": notifications_sent}


@shared_task
def send_document_review_reminders():
    today = timezone.localdate()
    review_horizon = today + timedelta(days=7)
    stale_cutoff = timezone.now() - timedelta(days=3)

    review_cycle_queryset = (
        ReviewCycle.objects.select_related("organization")
        .filter(next_review_date__isnull=False, next_review_date__gte=today, next_review_date__lte=review_horizon)
        .exclude(status__in=("completed", "archived"))
        .order_by("next_review_date", "id")
    )

    pending_document_queryset = (
        GeneratedDocument.objects.select_related("organization")
        .filter(generated_on__lte=stale_cutoff, status__in=("generated", "in_review"))
        .order_by("generated_on", "id")
    )

    notifications_sent = 0

    for cycle in review_cycle_queryset:
        dispatch_notification(
            title="Review cycle due soon",
            message=f"{cycle.title} should be reviewed by {cycle.next_review_date}.",
            organization=cycle.organization,
            source="review_cycle_reminder",
            send_email=True,
        )
        notifications_sent += 1

    for document in pending_document_queryset:
        dispatch_notification(
            title="Generated document awaiting decision",
            message=f"{document.title} ({document.version_label}) is still pending review or approval.",
            organization=document.organization,
            source="generated_document_reminder",
            send_email=True,
        )
        notifications_sent += 1

    return {"notifications_sent": notifications_sent}
