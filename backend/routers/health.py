from flask import Blueprint, jsonify
from datetime import datetime

bp = Blueprint("health", __name__)

@bp.route("/health", methods=["GET"])
def health_check():
    """Health-check endpoint"""
    return jsonify({
        "status": "ok",
        "time": datetime.utcnow().isoformat() + "Z",
        "message": "Service is running"
    }), 200
