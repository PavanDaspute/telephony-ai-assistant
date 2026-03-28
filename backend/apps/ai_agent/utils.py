"""
Utility helpers for the AI agent.
"""

from typing import List


# ─── Intent keyword maps ───────────────────────────────────────────────────────

INTENT_KEYWORDS = {
    "price": [
        "price", "cost", "rate", "how much", "budget", "lakh", "crore", "rupee",
        "affordable", "expensive", "cheap",
    ],
    "area": [
        "area", "size", "sqft", "sq ft", "square feet", "carpet", "how big", "how large",
    ],
    "location": [
        "location", "where", "address", "locality", "area", "city", "district",
        "nearby", "situated", "place",
    ],
    "amenities": [
        "amenities", "facilities", "features", "gym", "pool", "parking", "club",
        "security", "lift", "elevator", "garden", "park", "playground",
    ],
    "bedrooms": [
        "bedroom", "bhk", "room", "1bhk", "2bhk", "3bhk", "4bhk", "studio",
        "configuration",
    ],
    "description": [
        "describe", "tell me about", "details", "overview", "about", "explain",
    ],
}


def detect_intent(query: str) -> str:
    """
    Detect the primary intent of a caller's query using keyword matching.

    Returns one of: 'price', 'area', 'location', 'amenities', 'bedrooms',
    'description', or 'general'.
    """
    query_lower = query.lower()
    scores = {intent: 0 for intent in INTENT_KEYWORDS}

    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in query_lower:
                scores[intent] += 1

    # Return the intent with the highest score (ties broken by dict order)
    best_intent = max(scores, key=lambda k: scores[k])
    return best_intent if scores[best_intent] > 0 else "general"


def format_amenities(amenities: List[str]) -> str:
    """
    Convert a list of amenity strings into a readable sentence.

    Example:
        ['swimming pool', 'gym', 'parking'] → 'swimming pool, gym, and parking'
    """
    if not amenities:
        return "no listed amenities"
    if len(amenities) == 1:
        return amenities[0]
    return ", ".join(amenities[:-1]) + f", and {amenities[-1]}"
