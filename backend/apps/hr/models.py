from django.db import models
from apps.core.models import SoftDeleteAuditModel


class Department(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="department_hr")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class JobTitle(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="jobtitle_hr")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class Staff(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="staff_hr")
    person = models.ForeignKey("people.Person", on_delete=models.CASCADE, null=False, blank=False, related_name="staff_person")
    department = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True, blank=True, related_name="staff_department")
    job_title = models.ForeignKey("JobTitle", on_delete=models.SET_NULL, null=True, blank=True, related_name="staff_job_title")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="active")
    contract_end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class Team(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="team_hr")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="active")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class TeamMember(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="teammember_hr")
    team = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="members")
    staff = models.ForeignKey("Staff", on_delete=models.CASCADE, related_name="team_memberships")
    role = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=50, default="active")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.team} - {self.staff}"


class StaffSkill(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="staffskill_hr")
    staff = models.ForeignKey("Staff", on_delete=models.CASCADE, related_name="skills")
    skill = models.ForeignKey("volunteers.Skill", on_delete=models.CASCADE, related_name="staff_links")
    proficiency = models.CharField(max_length=80, blank=True)
    status = models.CharField(max_length=50, default="active")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.staff} - {self.skill}"


class TrainingCourse(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="trainingcourse_hr")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class Certificate(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="certificate_hr")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class TrainingEvent(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="trainingevent_hr")
    training_course = models.ForeignKey("TrainingCourse", on_delete=models.SET_NULL, null=True, blank=True, related_name="events")
    certificate = models.ForeignKey("Certificate", on_delete=models.SET_NULL, null=True, blank=True, related_name="training_events")
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default="planned")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)


class TrainingParticipant(SoftDeleteAuditModel):
    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="trainingparticipant_hr")
    training_event = models.ForeignKey("TrainingEvent", on_delete=models.CASCADE, related_name="participants")
    staff = models.ForeignKey("Staff", on_delete=models.CASCADE, related_name="training_participations")
    completion_status = models.CharField(max_length=50, default="registered")
    score = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    certificate_awarded = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.training_event} - {self.staff}"
