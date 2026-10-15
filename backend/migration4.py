from app import create_app
from models import db, ChatHistory

app = create_app()

with app.app_context():
    # Create new table ChatHistory
    db.create_all()
    print("Migration 4 complete")
