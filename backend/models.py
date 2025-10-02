from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))
    preferred_language = db.Column(db.String(50), default="English")  # e.g., "Hindi"
    industry = db.Column(db.String(50), default="general")  # e.g., "banking", "ecommerce"

    # Relationship → One user has many conversations
    conversations = db.relationship(
        "Conversation",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )
    analytics = db.relationship("Analytics", back_populates="user", uselist=False)  # One-to-one

    def __repr__(self):
        return f"<User {self.email} ({self.name})>"

class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    role = db.Column(db.String(10), nullable=False, default="user")  # 'user' or 'bot' (legacy)
    message = db.Column(db.Text, nullable=False)  # Original message summary
    intent = db.Column(db.String(50), default="unknown")  # e.g., "query", "complaint"
    sentiment_score = db.Column(db.Float, default=0.0)  # 0-1, positive/negative
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship back to User
    user = db.relationship("User", back_populates="conversations")

    # Relationship → One conversation has many messages
    messages = db.relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Conversation {self.intent}: {self.message[:20]}...>"

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id"), nullable=False)
    sender = db.Column(db.String(50), nullable=False)  # 'user' or 'bot'
    text = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), default="English")  # Detected lang
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship back to Conversation
    conversation = db.relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return f"<Message {self.sender}: {self.text[:20]}... ({self.language})>"

# New: Analytics model for aggregated metrics
class Analytics(db.Model):
    __tablename__ = "analytics"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    avg_sentiment = db.Column(db.Float, default=0.0)
    avg_response_time = db.Column(db.Float, default=0.0)
    escalation_count = db.Column(db.Integer, default=0)
    total_conversations = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="analytics")

    User.analytics = db.relationship("Analytics", back_populates="user", uselist=False)  # One-to-one
    user = db.relationship("User", back_populates="analytics")
    def __repr__(self):
        return f"<Analytics for User {self.user_id}: Avg Sentiment {self.avg_sentiment}>"