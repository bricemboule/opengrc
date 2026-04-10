from django.contrib import admin
from .models import (
    Certificate,
    Department,
    JobTitle,
    Staff,
    StaffSkill,
    Team,
    TeamMember,
    TrainingCourse,
    TrainingEvent,
    TrainingParticipant,
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "status", "organization")
    search_fields = ("code", "name")


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "status", "organization")
    search_fields = ("code", "name")


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "organization", "department", "job_title", "contract_end_date", "status")
    search_fields = ("code", "name")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "organization", "status")
    search_fields = ("code", "name")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "team", "staff", "role", "status")
    search_fields = ("team__name", "staff__name", "role")


@admin.register(StaffSkill)
class StaffSkillAdmin(admin.ModelAdmin):
    list_display = ("id", "staff", "skill", "proficiency", "status")
    search_fields = ("staff__name", "skill__name", "proficiency")


@admin.register(TrainingCourse)
class TrainingCourseAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "organization", "status")
    search_fields = ("code", "name")


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "organization", "status")
    search_fields = ("code", "name")


@admin.register(TrainingEvent)
class TrainingEventAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "training_course", "certificate", "start_date", "status")
    search_fields = ("code", "name")


@admin.register(TrainingParticipant)
class TrainingParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "training_event", "staff", "completion_status", "certificate_awarded")
    search_fields = ("training_event__name", "staff__name")
