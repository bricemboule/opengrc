import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from apps.accounts.models import User

from .models import Notification

logger = logging.getLogger(__name__)


def serialize_notification(notification):
    return {
        "id": notification.id,
        "title": notification.title,
        "message": notification.message,
        "source": notification.source,
        "receivedAt": notification.created_at.isoformat(),
        "deliveredAt": notification.delivered_at.isoformat() if notification.delivered_at else None,
    }


def push_notification_to_user(user_id, payload):
    channel_layer = get_channel_layer()
    if not channel_layer:
        return False

    try:
        async_to_sync(channel_layer.group_send)(
            f"notifications_user_{user_id}",
            {"type": "broadcast_notification", "notification": payload},
        )
        return True
    except Exception:  # pragma: no cover - runtime guard
        logger.exception("Unable to push realtime notification to user %s", user_id)
        return False


def send_notification_email(notification, subject=None):
    recipient_email = getattr(notification.recipient, "email", "")
    if not recipient_email:
        return Notification.EmailStatus.NOT_REQUESTED, None

    try:
        send_mail(
            subject or notification.title or "OpenGRC notification",
            notification.message,
            getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@opengrc.local"),
            [recipient_email],
            fail_silently=False,
        )
        return Notification.EmailStatus.SENT, None
    except Exception as exc:  # pragma: no cover - runtime guard
        logger.exception("Unable to send notification email to %s", recipient_email)
        return Notification.EmailStatus.FAILED, str(exc)


def get_notification_recipients(organization=None):
    recipients = User.objects.filter(is_active=True)
    if organization is not None:
        recipients = recipients.filter(organization=organization)
    else:
        recipients = recipients.exclude(organization__isnull=True)
    return recipients.distinct().order_by("id")


def dispatch_notification(message, organization=None, title="", source="system", send_email=True):
    recipients = list(get_notification_recipients(organization))
    if not recipients:
        return []

    notifications = []
    for user in recipients:
        notification = Notification.objects.create(
            organization=organization or user.organization,
            recipient=user,
            title=title,
            message=message,
            source=source,
        )

        delivered_at = timezone.now() if push_notification_to_user(user.id, serialize_notification(notification)) else None
        email_status = Notification.EmailStatus.NOT_REQUESTED
        email_error = ""
        emailed_at = None

        if send_email:
            email_status, email_error = send_notification_email(notification, subject=title or "OpenGRC notification")
            if email_status == Notification.EmailStatus.SENT:
                emailed_at = timezone.now()

        update_fields = []
        if delivered_at:
            notification.delivered_at = delivered_at
            update_fields.append("delivered_at")
        if email_status != Notification.EmailStatus.NOT_REQUESTED:
            notification.email_status = email_status
            notification.email_error = email_error or ""
            update_fields.extend(["email_status", "email_error"])
        if emailed_at:
            notification.emailed_at = emailed_at
            update_fields.append("emailed_at")
        if update_fields:
            notification.save(update_fields=update_fields)

        notifications.append(notification)

    return notifications
