import logging

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task
def send_email_notification(recipient, subject, body):
    try:
        send_mail(
            subject or "OpenGRC notification",
            body,
            getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@opengrc.local"),
            [recipient],
            fail_silently=False,
        )
        logger.info("Email sent to %s | subject=%s", recipient, subject)
        return {"recipient": recipient, "subject": subject, "status": "sent"}
    except Exception as exc:  # pragma: no cover - runtime guard
        logger.exception("Unable to send email to %s", recipient)
        return {"recipient": recipient, "subject": subject, "status": "failed", "error": str(exc)}


@shared_task
def send_sms_notification(recipient, message):
    logger.info("Sending SMS to %s", recipient)
    return {"recipient": recipient, "message": message, "status": "queued"}


@shared_task
def push_realtime_notification(message, user_id=None, notification=None):
    channel_layer = get_channel_layer()
    if not channel_layer:
        return {"status": "skipped", "message": message}

    payload = notification or {"message": message}
    group_name = f"notifications_user_{user_id}" if user_id else "global_notifications"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {"type": "broadcast_notification", "notification": payload, "message": message},
    )
    return {"status": "pushed", "message": message, "group": group_name}
