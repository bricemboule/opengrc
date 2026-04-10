from django.db import models
from apps.core.models import SoftDeleteAuditModel


class Member(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="member_memberships")
    person = models.ForeignKey("people.Person", on_delete=models.CASCADE, null=False, blank=False, related_name="member_person")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class Subscription(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="subscription_memberships")
    member = models.ForeignKey("Member", on_delete=models.CASCADE, null=False, blank=False, related_name="subscription_member")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)
