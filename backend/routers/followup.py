# backend/routers/followup.py
"""
Follow-up endpoint for automated post-chat surveys (email/SMS).
Generates content via Gemini, mocks send.
"""

import logging
import json
from flask import Blueprint, request, jsonify
from backend.models import db, Conversation
import google.generativeai as genai
import os
import smtplib  # For mock email
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

followup_bp = Blueprint("followup", __name__)

@followup_bp.route("/followup", methods=["POST"])
def generate_followup():
    """
    Generate and 'send' follow-up based on last conversation.
    Expects {"user_id": 1, "channel": "email" or "sms"}.
    """
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"error": "user_id required"}), 400

    user_id = data["user_id"]
    channel = data.get("channel", "email")  # Default email

    # Get last conv
    last_conv = Conversation.query.filter_by(user_id=user_id).order_by(Conversation.timestamp.desc()).first()
    if not last_conv:
        return jsonify({"error": "No conversation found"}), 404

    try:
        # Safe access to language
        lang = "English"  # Default
        if last_conv.messages:
            lang = last_conv.messages[0].language if last_conv.messages[0].language else "English"

        # Generate survey text via Gemini
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
        Generate a short satisfaction survey follow-up in {lang}.
        Reference recent issue: {last_conv.message[:100]} (intent: {last_conv.intent}).
        Include 1 question (e.g., "How satisfied were you? 1-5") and reply instructions.
        Format: {"email" if channel == "email" else "sms"} friendly.
        """
        response = model.generate_content(prompt)
        followup_text = response.text.strip()

        # Mock send
        if channel == "email":
            # Mock SMTP (no real send; log/print)
            msg = MIMEText(followup_text)
            msg['Subject'] = 'Customer Service Follow-Up'
            msg['From'] = 'support@example.com'
            msg['To'] = 'user@example.com'
            logger.info(f"Mock email sent: {followup_text[:100]}...")
            print(f"Mock Email Body: {followup_text}")  # Simulate send
        else:  # SMS
            logger.info(f"Mock SMS sent: {followup_text[:100]}...")
            print(f"Mock SMS: {followup_text}")  # Twilio mock

        return jsonify({
            "followup_text": followup_text,
            "channel": channel,
            "conversation_id": last_conv.id
        }), 200

    except Exception as e:
        logger.error(f"Follow-up generation error: {str(e)}")
        return jsonify({"error": "Failed to generate follow-up"}), 500