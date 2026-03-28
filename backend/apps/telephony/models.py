"""
Conversation log model for tracking call interactions.
"""

from django.db import models


class ConversationLog(models.Model):
    """
    Stores each voice interaction — the caller's query and the AI's response.
    """

    call_sid = models.CharField(max_length=64, blank=True, help_text="Twilio CallSid identifier")
    caller = models.CharField(max_length=32, blank=True, help_text="Caller phone number")
    user_query = models.TextField(help_text="What the caller asked")
    ai_response = models.TextField(help_text="Response returned by the AI agent")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Conversation Log"
        verbose_name_plural = "Conversation Logs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.created_at:%Y-%m-%d %H:%M}] {self.caller}: {self.user_query[:60]}"
