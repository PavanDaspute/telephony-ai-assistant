"""
Twilio webhook views for the voice telephony flow.

Endpoints:
  POST /voice/           — Initial webhook. Returns TwiML greeting + Gather.
  POST /process-speech/  — Receives SpeechResult, queries AI, returns TwiML response.
"""

import logging
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.conf import settings

from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse, Dial, Client

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

    def get(self, request, *args, **kwargs):
        return self._handle_request(request)

    def post(self, request, *args, **kwargs):
        return self._handle_request(request)

    def _handle_request(self, request):
        # Extract speech transcription and call metadata from Twilio
        data = request.POST if request.method == "POST" else request.GET
        print(data)
        speech_result = data.get("SpeechResult", "").strip()
        call_sid = data.get("CallSid", "")
        caller = data.get("From", "")

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


@method_decorator(csrf_exempt, name="dispatch")
class TokenView(View):
    """
    GET/POST /api/token/
    Generates a Twilio Access Token with VoiceGrant for browser-based calling.
    """

    def get(self, request, *args, **kwargs):
        return self._generate_token()

    def post(self, request, *args, **kwargs):
        return self._generate_token()

    def _generate_token(self):
        # Create an Access Token
        print(settings.TWILIO_ACCOUNT_SID)
        print(settings.TWILIO_API_KEY)
        print(settings.TWILIO_API_SECRET)
        print(settings.TWILIO_TWIML_APP_SID)
        token = AccessToken(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_API_KEY,
            settings.TWILIO_API_SECRET,
            identity="browser_user",
        )

        # Create a Voice grant and add to token
        grant = VoiceGrant(
            outgoing_application_sid=settings.TWILIO_TWIML_APP_SID,
            incoming_allow=True,  # Allow receiving calls
        )
        token.add_grant(grant)

        # Return token as JWT
        return JsonResponse({"token": token.to_jwt()})


@method_decorator(csrf_exempt, name="dispatch")
class OutgoingCallView(View):
    """
    POST /voice/outgoing/
    Twilio calls this when the browser app initiates a connection.
    We just dial the client identity so they can connect, and then
    the /voice/ endpoint usually handles the rest, or we directly
    return the welcome payload if we want it to start immediately.
    We'll route it back to ourselves so the caller hears the greeting.
    """

    def post(self, request, *args, **kwargs):
        # The frontend calls `device.connect({ params: { To: "browser_user" } })`
        # which eventually hits here. We need to answer the call and give them
        # the same TwiML as an incoming phone call would get.
        
        process_url = request.build_absolute_uri(reverse("process-speech"))
        twiml = build_welcome_twiml(gather_url=process_url)

        return HttpResponse(twiml, content_type="application/xml")
