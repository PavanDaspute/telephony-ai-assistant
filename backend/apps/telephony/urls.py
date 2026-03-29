"""
URL routes for Twilio webhook endpoints.
"""

from django.urls import path
from .views import VoiceWebhookView, ProcessSpeechView, TokenView, OutgoingCallView

urlpatterns = [
    path("voice/", VoiceWebhookView.as_view(), name="voice-webhook"),
    path("voice/outgoing/", OutgoingCallView.as_view(), name="voice-outgoing"),
    path("process-speech/", ProcessSpeechView.as_view(), name="process-speech"),
    path("api/token/", TokenView.as_view(), name="api-token"),
]
