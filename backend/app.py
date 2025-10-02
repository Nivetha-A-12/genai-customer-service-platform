"""
Entry point for the Flask app.

Run with:
    python -m backend.app
"""

import os
from flask import Flask, jsonify
from backend.config import Config
from backend.routers.health import bp as health_bp
from backend.routers.chat import chat_bp
from backend.routers.followup import followup_bp  # New
from backend.routers.analytics import analytics_bp  # New
from backend.models import db


def create_app():
    """Application factory to create Flask app instance"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize SQLAlchemy
    db.init_app(app)

    # register API blueprints under /api
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(chat_bp, url_prefix="/api")
    app.register_blueprint(followup_bp, url_prefix="/api")  # New
    app.register_blueprint(analytics_bp, url_prefix="/api")  # New
    
    @app.route("/", methods=["GET"])
    def index():
        return jsonify({"message": "GenAI Customer Service (Step 4)"}), 200

    return app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=True)