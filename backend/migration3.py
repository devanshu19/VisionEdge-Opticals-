from app import create_app
from models import db, VirtualTryOnHistory
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Add vto_image column if it doesn't exist (ignoring error if it does)
    try:
        db.session.execute(text('ALTER TABLE frame ADD COLUMN vto_image VARCHAR(255)'))
        db.session.commit()
    except Exception as e:
        print("Column vto_image might already exist:", e)
        db.session.rollback()

    # Create new table VirtualTryOnHistory
    db.create_all()
    print("Migration 3 complete")
