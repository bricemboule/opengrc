from django.db import models
from apps.core.models import SoftDeleteAuditModel


class Budget(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="budget_finance")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class Transaction(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="transaction_finance")
    budget = models.ForeignKey("Budget", on_delete=models.SET_NULL, null=True, blank=True, related_name="transaction_budget")
    reference = models.CharField(max_length=80, unique=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)
