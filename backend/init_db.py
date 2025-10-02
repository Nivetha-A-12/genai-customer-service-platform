# backend/init_db.py
from backend.models import db
from backend.app import create_app

app = create_app()

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    print("Creating all tables...")
    db.create_all()
    print("✅ Database schema created successfully!")