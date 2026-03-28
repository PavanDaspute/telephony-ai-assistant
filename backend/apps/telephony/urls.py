"""
URL routes for Twilio webhook endpoints.
"""

from django.urls import path
from .views import VoiceWebhookView, ProcessSpeechView

urlpatterns = [
    path("voice/", VoiceWebhookView.as_view(), name="voice-webhook"),
    path("process-speech/", ProcessSpeechView.as_view(), name="process-speech"),
]
