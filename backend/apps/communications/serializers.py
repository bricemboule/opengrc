from apps.core.serializers import AuditFieldsSerializerMixin
from .models import Message

class MessageSerializer(AuditFieldsSerializerMixin):
    class Meta:
        model = Message
        fields = "__all__"
