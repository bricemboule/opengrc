import logging

from django.db import transaction

from apps.communications.notifications import dispatch_notification

logger = logging.getLogger(__name__)


def _dispatch_notification_safely(**kwargs):
    try:
        dispatch_notification(**kwargs)
    except Exception:  # pragma: no cover - runtime guard
        logger.exception("Unable to dispatch Cyber GRC notification")


def broadcast_notification(message, organization=None, title="Cyber GRC alert", source="cybergrc", send_email=True):
    transaction.on_commit(
        lambda: _dispatch_notification_safely(
            message=message,
            organization=organization,
            title=title,
            source=source,
            send_email=send_email,
        )
    )
