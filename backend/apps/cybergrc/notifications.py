import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)


def broadcast_notification(message):
    channel_layer = get_channel_layer()
    if not channel_layer:
        return

    try:
        async_to_sync(channel_layer.group_send)(
            "global_notifications",
            {"type": "broadcast_notification", "message": message},
        )
    except Exception:  # pragma: no cover - defensive runtime guard
        logger.exception("Unable to broadcast realtime notification")

