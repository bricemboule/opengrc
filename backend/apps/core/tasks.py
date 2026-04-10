from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from apps.core.audit_models import AuditLog

@shared_task
def cleanup_soft_deleted_records():
    cutoff = timezone.now() - timedelta(days=90)
    deleted_count = AuditLog.objects.filter(created_at__lt=cutoff).count()
    return {"deleted_audit_logs": deleted_count}
