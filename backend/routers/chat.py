# backend/routers/chat.py
"""
Chat endpoint for GenAI-powered customer service.
Handles multilingual text queries using Google Gemini as primary model.
Stores conversations in PostgreSQL for context maintenance.
Includes auto-resolution via KB and escalation logic.
"""

import logging
import os
import time  # For basic timing (analytics teaser)
import json  # For parsing Gemini's structured output
import re  # For script-based language detection
from flask import Blueprint, request, jsonify
from backend.models import db, User, Conversation, Message
from backend.knowledge_base import find_resolution  # New import

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chat.log', encoding='utf-8'),  # UTF-8 for logs
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Google GenAI (Gemini) - Primary model (PaLM successor)
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

chat_bp = Blueprint("chat", __name__)

def get_gemini_model():
    """Initialize and return Gemini model for chat."""
    return genai.GenerativeModel("gemini-2.0-flash")  # Stable, multilingual model

def detect_language_by_script(text):
    """Detect language via Unicode script ranges (no external libs)."""
    if not text:
        return "English"
    
    # Regex for major Indian scripts (simplified)
    scripts = {
        r'[a-zA-Z]': "English",  # Latin fallback first to avoid override
        r'[\u0900-\u097F]': "Hindi",  # Devanagari (Hindi, Marathi) - Refined to Hindi
        r'[\u0B80-\u0BFF]': "Tamil",
        r'[\u0C00-\u0C7F]': "Telugu",
        r'[\u0C80-\u0CFF]': "Gujarati",
        r'[\u0980-\u09FF]': "Bengali"
    }
    
    for pattern, lang in scripts.items():
        if re.search(pattern, text):
            return lang
    return "Regional Indian"  # Catch-all

def get_conversation_history(user_id, limit=5):
    """Fetch recent conversation history for context."""
    convos = Conversation.query.filter_by(user_id=user_id).order_by(Conversation.timestamp.desc()).limit(limit).all()
    history = []
    for conv in convos:
        for msg in conv.messages:
            history.append(f"{msg.sender.capitalize()}: {msg.text[:50]}...")
    return " | ".join(reversed(history))  # Chronological

def infer_industry(user_text, current_industry="general"):
    """Simple heuristic to set industry based on keywords."""
    banking_keywords = ["account", "balance", "खाता", "बैलेंस", "लॉक", "lock"]
    if any(kw.lower() in user_text.lower() for kw in banking_keywords):
        return "banking"
    return current_industry

@chat_bp.route("/chat", methods=["POST"])
def chat():
    """
    Handle incoming chat message with context & personalization.
    - Fetches user history for context-aware responses.
    - Personalizes based on user profile (name, industry).
    - Detects language via script analysis or Gemini.
    - Generates structured response using Gemini.
    - Auto-resolves via KB if match; escalates if needed.
    - Stores with intent, sentiment, language.
    - Returns response under 5s.
    """
    data = request.get_json()
    if not data or "message" not in data:
        logger.error("Invalid request: Missing 'message' in JSON")
        return jsonify({"error": "Message is required"}), 400

    user_text = data["message"].strip()
    if not user_text:
        logger.warning("Empty message received")
        return jsonify({"error": "Empty message not allowed"}), 400

    user_id = data.get("user_id", None)  # Optional; fallback to test user

    # --- Get or Create User ---
    if user_id:
        user = User.query.get(user_id)
    else:
        user = User.query.filter_by(email="test@example.com").first()
    if not user:
        user = User(email=f"user_{int(time.time())}@example.com", name="Test User", industry="general")
        db.session.add(user)
        db.session.commit()
        logger.info(f"Created new user ID: {user.id}")

    # Infer and update industry if needed
    inferred_industry = infer_industry(user_text, user.industry)
    if inferred_industry != user.industry:
        user.industry = inferred_industry
        db.session.commit()
        logger.info(f"Updated user industry to: {inferred_industry}")

    # Debug text integrity
    logger.info(f"Incoming message (len={len(user_text)}, first_ord={ord(user_text[0]) if user_text else 'N/A'}): {user_text[:100]}...")

    detected_language = detect_language_by_script(user_text)
    logger.info(f"Script-detected language: {detected_language}")

    # Update user's preferred language if detected
    if detected_language != user.preferred_language:
        user.preferred_language = detected_language
        db.session.commit()
        logger.info(f"Updated user preferred lang to: {detected_language}")

    # Get history for context
    history = get_conversation_history(user.id)
    logger.info(f"History summary: {history[:200]}...")

    start_time = time.time()  # For response time tracking
    bot_reply = None
    intent = "unknown"
    sentiment_score = 0.0
    error_msg = None
    escalate = False
    context_summary = ""

    # --- Generate response with Gemini (context + personalization + structured) ---
    try:
        model = get_gemini_model()
        system_prompt = f"""
        You are a helpful, empathetic customer service assistant for {user.industry} industry.
        - Personalize: Greet as "Hello {user.name}!" if appropriate.
        - Always respond in the SAME language as the user's message (detect automatically: support English, Hindi, Tamil, Telugu, Marathi, Bengali, Gujarati).
        - Use context from history: {history}
        - Be concise, professional, and solution-oriented. Suggest resolutions from common knowledge if possible.
        - Classify intent accurately: 'query' for info requests (e.g., 'what is balance?'), 'complaint' for problems/issues (e.g., 'account locked', 'failed payment'), 'escalate' for requests to human or complex, 'unknown' otherwise.
        - Sentiment: 0.0-1.0 score, higher=positive (e.g., frustration=low).
        IMPORTANT: Respond ONLY in this exact JSON format (no extra text or markdown):
        {{
          "language": "Detected language name (e.g., 'Hindi', 'English')",
          "reply": "Your full response here",
          "intent": "query/complaint/escalate/unknown",
          "sentiment_score": 0.8  # Float 0.0-1.0
        }}
        """
        
        # Prompt with user text
        full_prompt = f"{system_prompt}\n\nUser message: {user_text}"
        
        response = model.generate_content(full_prompt)
        raw_response = response.text.strip()
        logger.info(f"Raw Gemini response: {raw_response}")  # For debug
        
        # Strip common markdown wrappers (e.g., ```json ... ```)
        raw_response = re.sub(r'^```json\s*|\s*```$', '', raw_response).strip()
        
        # Parse JSON
        try:
            parsed = json.loads(raw_response)
            gemini_lang = parsed.get("language", detected_language)
            bot_reply = parsed.get("reply", raw_response).strip()
            intent = parsed.get("intent", "unknown")
            sentiment_score = float(parsed.get("sentiment_score", 0.0))
            # Prioritize Gemini's lang if parsed
            detected_language = gemini_lang
        except json.JSONDecodeError:
            # Fallback if not JSON (rare)
            logger.warning("Gemini didn't return JSON; using raw")
            bot_reply = raw_response
            # Enhance fallback with script (already set above)
        
        logger.info(f"Final reply: {bot_reply[:100]}... (Intent: {intent}, Sentiment: {sentiment_score}, Lang: {detected_language})")
        
    except Exception as e:
        error_msg = f"Gemini error: {str(e)}"
        logger.error(error_msg)

    if not bot_reply:
        logger.error(f"Failed to generate response: {error_msg or 'Unknown error'}")
        return jsonify({"error": error_msg or "No response generated"}), 500

    # --- Auto-Resolution via KB ---
    resolution = find_resolution(intent, user_text, user.industry)
    if resolution and sentiment_score > 0.5:
        bot_reply = resolution  # Override with KB (Gemini will translate in UI if needed)
        logger.info(f"Auto-resolved via KB: {resolution[:50]}...")
    elif intent == "escalate" or sentiment_score < 0.3:
        escalate = True
        context_summary = f"User: {user.name} ({user.id}), History: {history[:200]}..., Current: {user_text}, Sentiment: {sentiment_score}"
        bot_reply = f"Escalating to human agent with context. Hold tight, {user.name}!"
        logger.info("Escalation triggered")

    response_time = time.time() - start_time
    if response_time > 5:
        logger.warning(f"Slow response detected: {response_time:.2f}s")

    logger.info(f"Response time: {response_time:.2f}s")

    # --- Store in DB ---
    try:
        # Create conversation entry
        conv = Conversation(
            user_id=user.id,
            role="user",  # Legacy; use intent now
            message=user_text,
            intent=intent,
            sentiment_score=sentiment_score
        )
        db.session.add(conv)
        db.session.commit()

        # Add messages with language
        msg_user = Message(conversation_id=conv.id, sender="user", text=user_text, language=detected_language)
        msg_bot = Message(conversation_id=conv.id, sender="bot", text=bot_reply, language=detected_language)
        db.session.add_all([msg_user, msg_bot])
        db.session.commit()

        logger.info(f"Stored conversation ID: {conv.id} (Intent: {intent}, Sentiment: {sentiment_score})")
    except Exception as db_e:
        logger.error(f"DB storage error: {db_e}")
        return jsonify({"error": "Failed to store conversation"}), 500

    # Build response
    response_data = {
        "user_message": user_text,
        "bot_reply": bot_reply,
        "detected_language": detected_language,
        "intent": intent,
        "sentiment_score": sentiment_score,
        "response_time": f"{response_time:.2f}s"
    }
    if escalate:
        response_data["escalate"] = True
        response_data["context_summary"] = context_summary

    return jsonify(response_data), 200