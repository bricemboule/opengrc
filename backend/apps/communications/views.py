from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet

from .models import Message, Notification
from .serializers import MessageSerializer, NotificationSerializer
from .tasks import push_realtime_notification, send_email_notification, send_sms_notification


class MessageViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Message.objects.select_related("organization").all()
    serializer_class = MessageSerializer
    search_fields = ["recipient", "subject", "status", "channel"]

    def perform_create(self, serializer):
        message = serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user,
            organization=getattr(self.request.user, "organization", None),
        )
        self.log_action("create", message)
        if message.channel == "email":
            result = send_email_notification(message.recipient, message.subject, message.body)
            message.status = result.get("status", "draft")
            message.save(update_fields=["status"])
        elif message.channel == "sms":
            result = send_sms_notification(message.recipient, message.body)
            message.status = result.get("status", "draft")
            message.save(update_fields=["status"])
        push_realtime_notification(f"New message for {message.recipient}")


class NotificationViewSet(ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "message", "source"]
    ordering_fields = ["created_at", "emailed_at", "delivered_at"]

    def get_queryset(self):
        return Notification.objects.select_related("organization", "recipient").filter(recipient=self.request.user).order_by("-created_at", "-id")

    @action(detail=True, methods=["post"], url_path="mark-read")
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        if not notification.is_read:
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save(update_fields=["is_read", "read_at"])
        return Response(self.get_serializer(notification).data)

    @action(detail=False, methods=["post"], url_path="mark-all-read")
    def mark_all_read(self, request):
        queryset = self.get_queryset().filter(is_read=False)
        updated = queryset.count()
        timestamp = timezone.now()
        queryset.update(is_read=True, read_at=timestamp)
        return Response({"updated": updated})
