from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from apps.core.viewsets import SoftDeleteAuditModelViewSet
from .models import Attachment
from .serializers import AttachmentSerializer


class AttachmentViewSet(SoftDeleteAuditModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
