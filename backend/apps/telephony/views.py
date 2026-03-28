"""
Twilio webhook views for the voice telephony flow.

Endpoints:
  POST /voice/           — Initial webhook. Returns TwiML greeting + Gather.
  POST /process-speech/  — Receives SpeechResult, queries AI, returns TwiML response.
"""

import logging
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse

from apps.ai_agent.services import get_ai_response
from .services import build_welcome_twiml, build_response_twiml
from .models import ConversationLog

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class VoiceWebhookView(View):
    """
    POST /voice/
    Twilio calls this endpoint when an incoming call is received.
    Returns TwiML that greets the caller and collects speech input.
    """

    def post(self, request, *args, **kwargs):
        # Build the absolute URL for the process-speech callback
        process_url = request.build_absolute_uri(reverse("process-speech"))
        print(request.POST)

        twiml = build_welcome_twiml(gather_url=process_url)

        return HttpResponse(twiml, content_type="application/xml")


@method_decorator(csrf_exempt, name="dispatch")
class ProcessSpeechView(View):
    """
    POST /process-speech/
    Twilio sends the SpeechResult here. We pass it to the AI agent,
    log the interaction, and return TwiML with the spoken answer.
    """

    def post(self, request, *args, **kwargs):
        # Extract speech transcription and call metadata from Twilio
        print(request.POST)
        speech_result = request.POST.get("SpeechResult", "").strip()
        call_sid = request.POST.get("CallSid", "")
        caller = request.POST.get("From", "")

        logger.warning("CallSid=%s | Caller=%s | Query=%s", call_sid, caller, speech_result)

        if not speech_result:
            fallback = "I could not understand your question. Please try again."
            process_url = request.build_absolute_uri(reverse("process-speech"))
            twiml = build_response_twiml(fallback, gather_url=process_url)
            return HttpResponse(twiml, content_type="application/xml")

        # Get AI-generated response from DB
        ai_response = get_ai_response(user_query=speech_result)

        # Log the conversation for analytics / audit
        ConversationLog.objects.create(
            call_sid=call_sid,
            caller=caller,
            user_query=speech_result,
            ai_response=ai_response,
        )

        # Build the callback URL for follow-up questions
        process_url = request.build_absolute_uri(reverse("process-speech"))
        twiml = build_response_twiml(ai_response, gather_url=process_url)

        return HttpResponse(twiml, content_type="application/xml")
