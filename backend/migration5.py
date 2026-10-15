from app import create_app
from models import db, Notification

app = create_app()

with app.app_context():
    # Create new table Notification
    db.create_all()
    print("Migration 5 complete")
