import logging
from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)

@shared_task
def send_email_notification(recipient, subject, body):
    logger.info("Sending email to %s | subject=%s", recipient, subject)
    return {"recipient": recipient, "subject": subject, "status": "sent"}

@shared_task
def send_sms_notification(recipient, message):
    logger.info("Sending SMS to %s", recipient)
    return {"recipient": recipient, "message": message, "status": "sent"}

@shared_task
def push_realtime_notification(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "global_notifications",
        {"type": "broadcast_notification", "message": message}
    )
    return {"status": "pushed", "message": message}
