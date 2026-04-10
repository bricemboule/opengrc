from django.db import models
from apps.core.models import SoftDeleteAuditModel


class Warehouse(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="warehouse_inventory")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class Stock(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="stock_inventory")
    warehouse = models.ForeignKey("Warehouse", on_delete=models.CASCADE, null=False, blank=False, related_name="stock_warehouse")
    sku = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class Shipment(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="shipment_inventory")
    warehouse = models.ForeignKey("Warehouse", on_delete=models.CASCADE, null=False, blank=False, related_name="shipment_warehouse")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class Adjustment(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="adjustment_inventory")
    warehouse = models.ForeignKey("Warehouse", on_delete=models.CASCADE, null=False, blank=False, related_name="adjustment_warehouse")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)
