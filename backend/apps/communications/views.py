from rest_framework.permissions import IsAuthenticated
from apps.core.tenancy import OrganizationScopedQuerySetMixin
from apps.core.viewsets import SoftDeleteAuditModelViewSet
from .models import Message
from .serializers import MessageSerializer
from .tasks import send_email_notification, send_sms_notification, push_realtime_notification

class MessageViewSet(OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet):
    queryset = Message.objects.select_related("organization").all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["recipient", "subject", "status", "channel"]

    def perform_create(self, serializer):
        message = serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user,
            organization=getattr(self.request.user, "organization", None),
        )
        self.log_action("create", message)
        if message.channel == "email":
            send_email_notification.delay(message.recipient, message.subject, message.body)
        elif message.channel == "sms":
            send_sms_notification.delay(message.recipient, message.body)
        push_realtime_notification.delay(f"Nouveau message pour {message.recipient}")
