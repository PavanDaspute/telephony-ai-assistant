"""
Django admin for ConversationLog — telephony interactions viewer.
"""

from django.contrib import admin
from .models import ConversationLog


@admin.register(ConversationLog)
class ConversationLogAdmin(admin.ModelAdmin):
    list_display = ["id", "caller", "call_sid", "user_query", "created_at"]
    search_fields = ["caller", "call_sid", "user_query", "ai_response"]
    readonly_fields = ["call_sid", "caller", "user_query", "ai_response", "created_at"]
    ordering = ["-created_at"]
