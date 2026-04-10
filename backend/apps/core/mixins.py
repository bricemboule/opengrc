from .audit_models import AuditLog

class AuditLogMixin:
    def log_action(self, action, instance, changes=None):
        request = getattr(self, "request", None)
        user = request.user if request and request.user.is_authenticated else None
        AuditLog.objects.create(
            user=user,
            action=action,
            model_name=instance.__class__.__name__,
            object_id=str(instance.pk),
            object_repr=str(instance),
            changes=changes or {},
        )
