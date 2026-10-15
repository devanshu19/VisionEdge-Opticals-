from app import create_app
from models import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Check if columns exist
        with db.engine.connect() as conn:
            # We use try/except block. If adding fails because it exists, we just ignore it.
            try:
                conn.execute(text("ALTER TABLE prescription ADD COLUMN prescription_image VARCHAR(255);"))
                print("Added prescription_image")
            except Exception as e:
                print(e)
                
            try:
                conn.execute(text("ALTER TABLE prescription ADD COLUMN ai_raw_text TEXT;"))
                print("Added ai_raw_text")
            except Exception as e:
                print(e)
                
            try:
                conn.execute(text("ALTER TABLE prescription ADD COLUMN confidence_score FLOAT;"))
                print("Added confidence_score")
            except Exception as e:
                print(e)
                
            conn.commit()
            print("Migration complete")
    except Exception as e:
        print("Fatal migration error:", e)
