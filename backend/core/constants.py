"""
Application-wide constants.
"""

# ─── Voice settings ────────────────────────────────────────────────────────────
# Twilio TTS voice for Indian English
DEFAULT_VOICE = "Polly.Aditi"

# Speech recognition language
DEFAULT_LANGUAGE = "en-IN"

# Maximum TTS character length to avoid overly long responses
MAX_RESPONSE_LENGTH = 500

# ─── Intent labels ─────────────────────────────────────────────────────────────
INTENT_PRICE = "price"
INTENT_AREA = "area"
INTENT_LOCATION = "location"
INTENT_AMENITIES = "amenities"
INTENT_BEDROOMS = "bedrooms"
INTENT_DESCRIPTION = "description"
INTENT_GENERAL = "general"

ALL_INTENTS = [
    INTENT_PRICE,
    INTENT_AREA,
    INTENT_LOCATION,
    INTENT_AMENITIES,
    INTENT_BEDROOMS,
    INTENT_DESCRIPTION,
    INTENT_GENERAL,
]
