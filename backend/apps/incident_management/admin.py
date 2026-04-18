from django.contrib import admin

from .models import (
    AssetAllocation,
    Incident,
    IncidentAssignment,
    IncidentAttachment,
    IncidentCommunication,
    IncidentTask,
    IncidentUpdate,
    SOPExecution,
    SOPExecutionStep,
    SOPStep,
    SOPTemplate,
)


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ("title", "incident_type", "severity", "status", "incident_coordinator", "reported_at")
    list_filter = ("incident_type", "severity", "status", "source", "national_significance")
    search_fields = ("title", "summary", "external_reference")
    filter_horizontal = ("affected_sectors", "affected_infrastructure")


@admin.register(IncidentUpdate)
class IncidentUpdateAdmin(admin.ModelAdmin):
    list_display = ("title", "incident", "update_type", "recorded_at")
    list_filter = ("update_type", "status_snapshot", "severity_snapshot")
    search_fields = ("title", "message")


@admin.register(IncidentTask)
class IncidentTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "incident", "status", "priority", "assigned_to", "due_at")
    list_filter = ("status", "priority")
    search_fields = ("title", "description", "blocker_summary")


@admin.register(IncidentAssignment)
class IncidentAssignmentAdmin(admin.ModelAdmin):
    list_display = ("incident", "role_in_response", "status", "assignee", "stakeholder", "assigned_at")
    list_filter = ("status",)
    search_fields = ("role_in_response", "notes")


@admin.register(IncidentCommunication)
class IncidentCommunicationAdmin(admin.ModelAdmin):
    list_display = ("subject", "incident", "direction", "channel", "sent_at", "requires_acknowledgement")
    list_filter = ("direction", "channel", "requires_acknowledgement")
    search_fields = ("subject", "audience", "message")


@admin.register(IncidentAttachment)
class IncidentAttachmentAdmin(admin.ModelAdmin):
    list_display = ("title", "incident", "attachment_type", "reference_label", "created_at")
    list_filter = ("attachment_type",)
    search_fields = ("title", "reference_label", "notes")


@admin.register(SOPTemplate)
class SOPTemplateAdmin(admin.ModelAdmin):
    list_display = ("title", "code", "status", "contingency_plan", "related_infrastructure", "last_reviewed_at")
    list_filter = ("status",)
    search_fields = ("title", "code", "objective", "activation_trigger")


@admin.register(SOPStep)
class SOPStepAdmin(admin.ModelAdmin):
    list_display = ("template", "step_order", "title", "step_type", "is_required", "default_assignee")
    list_filter = ("step_type", "is_required")
    search_fields = ("title", "instruction", "responsible_role")


@admin.register(SOPExecution)
class SOPExecutionAdmin(admin.ModelAdmin):
    list_display = ("title", "incident", "template", "status", "execution_commander", "started_at", "completed_at")
    list_filter = ("status", "template")
    search_fields = ("title", "summary", "outcome_summary", "blocker_summary")


@admin.register(SOPExecutionStep)
class SOPExecutionStepAdmin(admin.ModelAdmin):
    list_display = ("execution", "step_order", "title", "status", "assigned_to", "completed_by")
    list_filter = ("status", "step_type", "is_required")
    search_fields = ("title", "instruction", "blocker_summary", "notes")


@admin.register(AssetAllocation)
class AssetAllocationAdmin(admin.ModelAdmin):
    list_display = ("title", "incident", "emergency_asset", "status", "priority", "quantity_allocated", "requested_at")
    list_filter = ("status", "priority")
    search_fields = ("title", "destination", "deployment_notes", "release_notes")
