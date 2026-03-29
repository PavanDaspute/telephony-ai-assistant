"""
AI Agent service: Google Gemini API integration with conversational memory.
"""

import logging
import os
import google.generativeai as genai
from apps.properties.models import Property

logger = logging.getLogger(__name__)

# Configure Gemini client
api_key = os.environ.get("GEMINI_API_KEY", "")
if api_key:
    genai.configure(api_key=api_key)

# In-memory conversation store mapping CallSid to message history
# Formats stored: {"role": "user"|"assistant", "content": "..."}
conversation_store = {}


def get_ai_response(user_query: str, call_sid: str = "default") -> str:
    """
    Main entry point for the AI agent using Google Gemini API.

    Args:
        user_query: Natural language question from the caller.
        call_sid: Twilio CallSid to maintain context for the call session.

    Returns:
        A natural language response string ready for TTS.
    """
    logger.info("Starting AI Response Generation | CallSid: %s", call_sid)
    
    query_lower = user_query.strip()
    if not query_lower:
        return "I didn't catch that. Could you please repeat your question?"

    # Fetch properties from DB and format as context
    properties = Property.objects.all()
    if not properties.exists():
        return (
            "I'm sorry, I don't have any property listings available at the moment. "
            "Please contact our office directly for more information."
        )

    # Format property data into a context string
    prop_data = []
    for prop in properties:
        prop_str = (
            f"- Title: '{prop.title}', Location: {prop.location}, "
            f"Price: {prop.price_in_lakhs()}, Area: {prop.carpet_area} sq ft, "
            f"Bedrooms: {prop.bedrooms}BHK, Amenities: {', '.join(prop.amenities)}"
        )
        prop_data.append(prop_str)
    
    properties_context = "\n".join(prop_data)

    # Initialize or get conversation history
    if call_sid not in conversation_store:
        conversation_store[call_sid] = []
        
    history = conversation_store[call_sid]

    # Format conversation history for prompt
    history_str = ""
    for msg in history:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_str += f"{role}: {msg['content']}\n"
    
    if not history_str:
        history_str = "No previous messages."

    # Construct the strict prompt as requested
    prompt = f"""You are a real estate voice assistant.

Rules:
* Answer ONLY using provided property data
* Do NOT make up information
* Keep response within 1-2 sentences
* Be conversational and clear

Property Details:
{properties_context}

Conversation History:
{history_str}

User Question: {query_lower}
"""

    try:
        if not api_key:
            return "Gemini API key is missing. Please contact the administrator."
            
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        response = model.generate_content(prompt)
        ai_reply = response.text.strip()
        logger.info("Gemini API call successful | CallSid: %s", call_sid)
        
        # Append to history
        history.append({"role": "user", "content": query_lower})
        history.append({"role": "assistant", "content": ai_reply})
        
        # Limit history to last 5 message pairs (10 messages total)
        if len(history) > 10:
            history = history[-10:]
            
        conversation_store[call_sid] = history
        
        return ai_reply
        
    except Exception as e:
        logger.error("Gemini API error: %s", e)
        return "I am currently experiencing technical difficulties. Please try again later."
