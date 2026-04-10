from django.db import models
from django.core.exceptions import ValidationError
from apps.core.models import SoftDeleteAuditModel
from apps.org.models import Organization

class Project(SoftDeleteAuditModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=80, unique=True)
    status = models.CharField(max_length=50, default="draft")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Activity(SoftDeleteAuditModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="activities")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="activities")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, default="planned")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    contact_person = models.ForeignKey("people.Person", on_delete=models.SET_NULL, null=True, blank=True, related_name="project_activities")
    estimated_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    actual_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name

    def clean(self):
        if self.project_id and self.organization_id and self.project.organization_id != self.organization_id:
            raise ValidationError({"project": "Le projet doit appartenir a la meme organisation."})
        if self.contact_person_id and self.organization_id and self.contact_person.organization_id != self.organization_id:
            raise ValidationError({"contact_person": "Le contact doit appartenir a la meme organisation."})
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "La date de fin doit etre posterieure a la date de debut."})


class Task(SoftDeleteAuditModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="tasks")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, default="new")
    priority = models.CharField(max_length=50, default="normal")
    assigned_to = models.ForeignKey("people.Person", on_delete=models.SET_NULL, null=True, blank=True, related_name="project_tasks")
    due_date = models.DateField(null=True, blank=True)
    estimated_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    actual_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    source = models.CharField(max_length=255, blank=True)
    source_url = models.URLField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title

    def clean(self):
        if self.project_id and self.organization_id and self.project.organization_id != self.organization_id:
            raise ValidationError({"project": "Le projet doit appartenir a la meme organisation."})
        if self.activity_id:
            if self.activity.organization_id != self.organization_id:
                raise ValidationError({"activity": "L'activite doit appartenir a la meme organisation."})
            if self.project_id and self.activity.project_id != self.project_id:
                raise ValidationError({"activity": "L'activite selectionnee n'appartient pas au projet."})
        if self.assigned_to_id and self.organization_id and self.assigned_to.organization_id != self.organization_id:
            raise ValidationError({"assigned_to": "Le responsable assigne doit appartenir a la meme organisation."})
