"""
VisionEdge — Application Configuration
======================================
Database Architecture: Supabase PostgreSQL
------------------------------------------
The primary database is Supabase PostgreSQL, accessed via standard
SQLAlchemy PostgreSQL connection string using the psycopg2 driver:

  DATABASE_URL=postgresql+psycopg2://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres

Optional fallback:
  SQLite fallback is supported strictly for offline local test suites
  when USE_SQLITE=true is explicitly set in .env.
"""

import os
import sys
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()


def _build_database_uri() -> str:
    """
    Determine the effective database URI.

    Priority:
      1. DATABASE_URL          (PostgreSQL URI from Supabase or any PG host)
      2. SUPABASE_DB_URL       (convenience alias)
      3. SQLite fallback       (only when USE_SQLITE=true for local offline tests)

    Rejects any legacy MySQL URI with an actionable configuration error.
    """
    database_url = os.getenv("DATABASE_URL", "").strip()
    supabase_db_url = os.getenv("SUPABASE_DB_URL", "").strip()
    use_sqlite = os.getenv("USE_SQLITE", "false").lower() == "true"

    # --- Resolve primary candidate ---
    uri = database_url or supabase_db_url

    if uri:
        # Normalize postgres:// or postgresql:// to postgresql+psycopg2://
        if uri.startswith("postgres://"):
            uri = "postgresql+psycopg2://" + uri[len("postgres://"):]
        elif uri.startswith("postgresql://") and "+psycopg" not in uri:
            uri = uri.replace("postgresql://", "postgresql+psycopg2://", 1)

        # Reject any leftover MySQL URI
        parsed = urlparse(uri)
        if parsed.scheme.startswith("mysql"):
            print(
                "\n[CONFIG ERROR] A legacy MySQL URI was supplied via DATABASE_URL / SUPABASE_DB_URL.\n"
                "VisionEdge has migrated to Supabase PostgreSQL.\n"
                "Please configure DATABASE_URL with a valid Supabase PostgreSQL connection string.\n",
                file=sys.stderr,
            )
            sys.exit(1)

        return uri

    # --- SQLite fallback (offline local dev / CI only) ---
    if use_sqlite:
        base_dir = os.path.abspath(os.path.dirname(__file__))
        sqlite_path = os.path.join(base_dir, "visionedge.db")
        return f"sqlite:///{sqlite_path}"

    # --- No usable URI found ---
    print(
        "\n[CONFIG ERROR] No database URI configured.\n"
        "Please set the DATABASE_URL environment variable to your Supabase PostgreSQL connection string.\n"
        "Example:\n"
        "  DATABASE_URL=postgresql+psycopg2://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres\n"
        "\nFor offline local testing only, you may set USE_SQLITE=true in .env.\n",
        file=sys.stderr,
    )
    base_dir = os.path.abspath(os.path.dirname(__file__))
    return f"sqlite:///{os.path.join(base_dir, 'visionedge.db')}"


class Config:
    # ------------------------------------------------------------------ #
    # Flask core
    # ------------------------------------------------------------------ #
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "86400"))  # 24 h

    # ------------------------------------------------------------------ #
    # Database (Supabase PostgreSQL)
    # ------------------------------------------------------------------ #
    SQLALCHEMY_DATABASE_URI: str = _build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Connection pool settings — tuned for Supabase Supavisor (transaction pooler)
    _is_postgres = SQLALCHEMY_DATABASE_URI.startswith("postgresql")
    SQLALCHEMY_ENGINE_OPTIONS: dict = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 5,
        "max_overflow": 10,
        **({"connect_args": {"sslmode": os.getenv("DB_SSLMODE", "require")}}
           if _is_postgres else {}),
    }

    # ------------------------------------------------------------------ #
    # Supabase Storage / API (optional — only needed for Storage features)
    # ------------------------------------------------------------------ #
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_PUBLISHABLE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY", "")

    # ------------------------------------------------------------------ #
    # Email / SMTP
    # ------------------------------------------------------------------ #
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_EMAIL = os.getenv("SMTP_EMAIL", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

    # ------------------------------------------------------------------ #
    # Payment
    # ------------------------------------------------------------------ #
    PAYU_KEY = os.getenv("PAYU_KEY", "gtKFFx")
    PAYU_SALT = os.getenv("PAYU_SALT", "eCwWELxi")
    PAYU_URL = os.getenv("PAYU_URL", "https://test.payu.in/_payment")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8000")

    # ------------------------------------------------------------------ #
    # Diagnostic helper (does not expose credentials)
    # ------------------------------------------------------------------ #
    @classmethod
    def db_dialect(cls) -> str:
        """Return the database dialect name without exposing credentials."""
        try:
            parsed = urlparse(cls.SQLALCHEMY_DATABASE_URI)
            return parsed.scheme.split("+")[0]  # e.g. 'postgresql', 'sqlite'
        except Exception:
            return "unknown"
