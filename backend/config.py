"""
Flask app configuration.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")
    DEBUG = os.environ.get("DEBUG", "1") == "1"
 # PostgreSQL connection
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/genai_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False