"""
Telephony service helpers.
"""

from twilio.twiml.voice_response import VoiceResponse, Gather
from django.conf import settings


def build_welcome_twiml(gather_url: str) -> str:
    """
    Build TwiML that greets the caller and opens a speech Gather.

    Args:
        gather_url: The callback URL for /process-speech/

    Returns:
        TwiML XML string.
    """
    response = VoiceResponse()

    gather = Gather(
        input="speech",
        action=gather_url,
        method="POST",
        speech_timeout="auto",
        language="en-IN",
    )
    gather.say(
        "Welcome to the property assistant. "
        "You can ask me about price, location, area, or amenities. "
        "Please speak your question after the tone.",
        voice="Polly.Aditi",  # Indian English TTS voice
    )
    response.append(gather)

    # Fallback if no speech detected
    response.say(
        "I did not receive any input. Please call back and try again.",
        voice="Polly.Aditi",
    )
    return str(response)


def build_response_twiml(ai_text: str, gather_url: str) -> str:
    """
    Build TwiML that speaks the AI response and asks if the caller
    has further questions.

    Args:
        ai_text: The AI-generated response to speak.
        gather_url: The callback URL for /process-speech/

    Returns:
        TwiML XML string.
    """
    response = VoiceResponse()
    response.say(ai_text, voice="Polly.Aditi")

    gather = Gather(
        input="speech",
        action=gather_url,
        method="POST",
        speech_timeout="auto",
        language="en-IN",
    )
    gather.say(
        "Do you have any other questions? Please go ahead.",
        voice="Polly.Aditi",
    )
    response.append(gather)

    response.say("Thank you for calling. Goodbye!", voice="Polly.Aditi")
    response.hangup()
    return str(response)
