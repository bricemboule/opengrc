from django.db import transaction

from apps.communications.notifications import dispatch_notification


def broadcast_notification(message, organization=None, title="Cyber GRC alert", source="cybergrc", send_email=True):
    transaction.on_commit(
        lambda: dispatch_notification(
            message=message,
            organization=organization,
            title=title,
            source=source,
            send_email=send_email,
        )
    )
