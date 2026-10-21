"""
manage.py — VisionEdge Database Management CLI
================================================
Usage (from the backend/ directory with venv activated):

  # Initialize Flask-Migrate (first time only):
  python manage.py db init

  # Generate a new migration after model changes:
  python manage.py db migrate -m "describe the change"

  # Apply pending migrations to the database:
  python manage.py db upgrade

  # Downgrade one revision:
  python manage.py db downgrade

  # Show current revision:
  python manage.py db current

  # Show migration history:
  python manage.py db history

  # Verify DB connection:
  python manage.py db_check

Note: DATABASE_URL must be set in .env before running migrations.
"""

import os
import sys

# Ensure backend/ is on the Python path when running from project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db
from flask_migrate import Migrate
from flask.cli import FlaskGroup

app = create_app()
migrate = Migrate(app, db)

cli = FlaskGroup(app)


@app.cli.command("db_check")
def db_check():
    """Verify the database connection without exposing credentials."""
    from sqlalchemy import text
    from config import Config
    dialect = Config.db_dialect()
    print(f"Configured dialect: {dialect}")
    try:
        with app.app_context():
            result = db.session.execute(text("SELECT 1"))
            result.close()
            print("✓ Database connection successful.")
    except Exception as e:
        print(f"✗ Database connection failed: {type(e).__name__}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
