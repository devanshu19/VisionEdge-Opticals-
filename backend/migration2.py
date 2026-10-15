from app import create_app
from models import db, FrameRecommendation

app = create_app()

with app.app_context():
    # create_all will create any missing tables, like frame_recommendation
    db.create_all()
    print("Migration 2 complete")
