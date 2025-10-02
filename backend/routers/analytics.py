# backend/routers/analytics.py
"""
Analytics endpoint for user performance metrics.
Aggregates from DB.
"""

import logging
from flask import Blueprint, jsonify
from backend.models import db, Conversation, Analytics
from sqlalchemy import func
from datetime import datetime  # Added for assignment

logger = logging.getLogger(__name__)

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics/<int:user_id>", methods=["GET"])
def get_analytics(user_id):
    """
    Get aggregated analytics for user.
    Updates/returns from Analytics table.
    """
    # Fetch raw data
    convs = Conversation.query.filter_by(user_id=user_id).all()
    if not convs:
        return jsonify({"error": "No data for user"}), 404

    sentiments = [c.sentiment_score for c in convs]
    avg_sentiment = sum(sentiments) / len(sentiments)
    escalations = sum(1 for c in convs if c.intent == "escalate")
    total_convs = len(convs)

    # Update or create Analytics entry
    anal = Analytics.query.filter_by(user_id=user_id).first()
    if not anal:
        anal = Analytics(user_id=user_id)
        db.session.add(anal)
    anal.avg_sentiment = avg_sentiment
    anal.escalation_count = escalations
    anal.total_conversations = total_convs
    anal.last_updated = datetime.utcnow()  # Fixed: Use datetime, not func.now()
    db.session.commit()

    return jsonify({
        "user_id": user_id,
        "avg_sentiment": round(avg_sentiment, 2),
        "avg_response_time": "N/A",  # Teaser; add timing field later if needed
        "escalation_rate": f"{escalations / total_convs * 100:.1f}%" if total_convs > 0 else "0.0%",
        "total_conversations": total_convs
    }), 200