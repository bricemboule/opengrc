from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "recipient", "channel", "status", "organization")
    search_fields = ("recipient", "subject", "status")
