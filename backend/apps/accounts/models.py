from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import SoftDeleteAuditModel

class User(AbstractUser, SoftDeleteAuditModel):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    is_verified = models.BooleanField(default=False)
    roles = models.ManyToManyField("rbac.Role", blank=True, related_name="users")
    organization = models.ForeignKey(
        "org.Organization", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="users"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def get_all_permissions(self, obj=None):
        direct_permissions = super().get_all_permissions(obj)
        role_permissions = set()
        for role in self.roles.prefetch_related("permissions").all():
            for perm in role.permissions.all():
                role_permissions.add(f"{perm.content_type.app_label}.{perm.codename}")
        return set(direct_permissions).union(role_permissions)
