"""
AI Agent service: intent detection + DB-driven natural language response generation.

This module is intentionally designed to be OpenAI-ready.
Currently uses a rule-based intent detector with DB lookups.
To enable OpenAI: set OPENAI_API_KEY in .env and switch the USE_OPENAI flag.
"""

import logging
from typing import Optional
from apps.properties.models import Property
from .utils import detect_intent, format_amenities

logger = logging.getLogger(__name__)

# Set to True and supply OPENAI_API_KEY to enable GPT-based responses
USE_OPENAI = False


def get_ai_response(user_query: str, property_id: Optional[int] = None) -> str:
    """
    Main entry point for the AI agent.

    Args:
        user_query: Natural language question from the caller.
        property_id: If provided, restricts DB lookup to this specific property.

    Returns:
        A natural language response string ready for TTS.
    """
    query_lower = user_query.lower().strip()

    if not query_lower:
        return "I didn't catch that. Could you please repeat your question?"

    # Fetch properties from DB
    if property_id:
        properties = Property.objects.filter(pk=property_id)
    else:
        properties = Property.objects.all()

    if not properties.exists():
        return (
            "I'm sorry, I don't have any property listings available at the moment. "
            "Please contact our office directly for more information."
        )

    # Detect caller intent from query text
    intent = detect_intent(query_lower)
    logger.info("Detected intent [%s] for query: %s", intent, user_query)

    # Route to the appropriate response builder
    if intent == "price":
        return _handle_price_query(properties, query_lower)
    elif intent == "area":
        return _handle_area_query(properties, query_lower)
    elif intent == "location":
        return _handle_location_query(properties)
    elif intent == "amenities":
        return _handle_amenities_query(properties, query_lower)
    elif intent == "bedrooms":
        return _handle_bedrooms_query(properties, query_lower)
    elif intent == "description":
        return _handle_description_query(properties, query_lower)
    else:
        return _handle_general_query(properties)


# ─── Intent handlers ──────────────────────────────────────────────────────────

def _handle_price_query(properties, query: str) -> str:
    """Respond to price-related questions."""
    # If the caller mentions a specific BHK, filter
    bhk_filter = _extract_bhk(query)
    if bhk_filter:
        matched = properties.filter(bedrooms=bhk_filter)
        if matched.exists():
            prop = matched.first()
            return (
                f"The {prop.bedrooms}BHK flat titled '{prop.title}' in {prop.location} "
                f"is priced at {prop.price_in_lakhs()}."
            )

    # Return all prices
    parts = []
    for prop in properties[:5]:
        parts.append(f"{prop.bedrooms}BHK in {prop.location}: {prop.price_in_lakhs()}")
    intro = "Here are the available prices: " if len(parts) > 1 else ""
    return intro + ". ".join(parts) + "."


def _handle_area_query(properties, query: str) -> str:
    """Respond to carpet area related questions."""
    bhk_filter = _extract_bhk(query)
    if bhk_filter:
        matched = properties.filter(bedrooms=bhk_filter)
        if matched.exists():
            prop = matched.first()
            return (
                f"The {prop.bedrooms}BHK flat in {prop.location} has a carpet area of "
                f"{prop.carpet_area} square feet."
            )

    parts = []
    for prop in properties[:5]:
        parts.append(f"{prop.bedrooms}BHK in {prop.location}: {prop.carpet_area} sq ft")
    return "Carpet areas available: " + ", ".join(parts) + "."


def _handle_location_query(properties) -> str:
    """Respond to location-related questions."""
    locations = list(properties.values_list("location", flat=True).distinct())
    if len(locations) == 1:
        return f"The property is located in {locations[0]}."
    location_str = ", ".join(locations[:-1]) + " and " + locations[-1]
    return f"We have properties in {location_str}."


def _handle_amenities_query(properties, query: str) -> str:
    """Respond to amenities-related questions."""
    bhk_filter = _extract_bhk(query)
    if bhk_filter:
        matched = properties.filter(bedrooms=bhk_filter)
        if matched.exists():
            prop = matched.first()
            amenities_str = format_amenities(prop.amenities)
            return f"The {prop.bedrooms}BHK in {prop.location} includes: {amenities_str}."

    # Aggregate all amenities from the first matching property
    prop = properties.first()
    amenities_str = format_amenities(prop.amenities)
    return f"The property in {prop.location} includes the following amenities: {amenities_str}."


def _handle_bedrooms_query(properties, query: str) -> str:
    """Respond to BHK / bedroom-related questions."""
    bhk_options = list(properties.values_list("bedrooms", flat=True).distinct().order_by("bedrooms"))
    options_str = " and ".join([f"{b}BHK" for b in bhk_options])
    return f"We currently have {options_str} configurations available."


def _handle_description_query(properties, query: str) -> str:
    """Respond to general description questions."""
    prop = properties.first()
    desc = prop.description.strip() if prop.description else "No additional description available."
    return desc[:500]  # Limit TTS length


def _handle_general_query(properties) -> str:
    """Fallback — summarise the first available property."""
    prop = properties.first()
    return (
        f"We have a {prop.bedrooms}BHK property called '{prop.title}' located in {prop.location}. "
        f"It is priced at {prop.price_in_lakhs()} and has a carpet area of {prop.carpet_area} square feet. "
        f"You can ask me about price, area, location, or amenities for more details."
    )


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _extract_bhk(query: str) -> Optional[int]:
    """Extract a BHK number from the query string, e.g. '2BHK' → 2."""
    import re
    match = re.search(r"(\d)\s*bhk", query, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None
