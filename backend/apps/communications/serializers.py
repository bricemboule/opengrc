from apps.core.serializers import AuditFieldsSerializerMixin

from .models import Message, Notification


class MessageSerializer(AuditFieldsSerializerMixin):
    class Meta:
        model = Message
        fields = "__all__"


class NotificationSerializer(AuditFieldsSerializerMixin):
    class Meta:
        model = Notification
        fields = [
            "id",
            "title",
            "message",
            "source",
            "is_read",
            "read_at",
            "delivered_at",
            "email_status",
            "emailed_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "title",
            "message",
            "source",
            "is_read",
            "read_at",
            "delivered_at",
            "email_status",
            "emailed_at",
            "created_at",
            "updated_at",
        ]
