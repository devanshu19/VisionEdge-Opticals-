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

_backend_env = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.getenv("APP_ENV", "").strip().lower() != "production":
    if os.path.exists(_backend_env):
        load_dotenv(_backend_env)
    else:
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
    is_production = os.getenv("APP_ENV", "").strip().lower() == "production"

    if is_production and not database_url:
        raise RuntimeError("DATABASE_URL is required in production; SQLite and SUPABASE_DB_URL fallback are disabled.")

    # --- Resolve primary candidate ---
    uri = database_url or supabase_db_url

    if uri:
        # If user accidentally put Supabase project HTTPS URL in DATABASE_URL, ignore it
        if uri.startswith("http://") or uri.startswith("https://"):
            if is_production:
                raise RuntimeError("DATABASE_URL must be a PostgreSQL connection URI in production.")
            print(
                "\n[CONFIG WARNING] An HTTP(S) URL was supplied for DATABASE_URL / SUPABASE_DB_URL.\n"
                "DATABASE_URL must be a PostgreSQL connection URI (e.g. postgresql+psycopg2://...),\n"
                "not the Supabase REST/Web endpoint. Ignoring and falling back to SQLite if enabled.\n",
                file=sys.stderr,
            )
            uri = ""
        else:
            # Normalize postgres:// or postgresql:// to postgresql+psycopg2://
            if uri.startswith("postgres://"):
                uri = "postgresql+psycopg2://" + uri[len("postgres://"):]
            elif uri.startswith("postgresql://") and "+psycopg" not in uri:
                uri = uri.replace("postgresql://", "postgresql+psycopg2://", 1)

            # Reject any leftover MySQL URI
            parsed = urlparse(uri)
            if is_production and parsed.scheme.split("+")[0] != "postgresql":
                raise RuntimeError("Production DATABASE_URL must use PostgreSQL; SQLite fallback is disabled.")
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
        if is_production:
            raise RuntimeError("USE_SQLITE cannot be enabled in production.")
        base_dir = os.path.abspath(os.path.dirname(__file__))
        sqlite_path = os.path.join(base_dir, "visionedge.db")
        return f"sqlite:///{sqlite_path}"

    # --- No usable URI found ---
    if is_production:
        raise RuntimeError("A valid PostgreSQL DATABASE_URL is required in production.")
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
    IS_PRODUCTION = os.getenv("APP_ENV", "").strip().lower() == "production"

    # ------------------------------------------------------------------ #
    # Flask core
    # ------------------------------------------------------------------ #
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.getenv("DEBUG", "false").strip().lower() in ("1", "true", "yes") and not IS_PRODUCTION

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
    PAYU_KEY = os.getenv("PAYU_KEY", "").strip()
    PAYU_SALT = os.getenv("PAYU_SALT", "").strip()
    PAYU_URL = os.getenv("PAYU_URL", "https://test.payu.in/_payment")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8000").strip().rstrip("/")
    CORS_ALLOWED_ORIGINS = tuple(
        origin.strip().rstrip("/")
        for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
        if origin.strip()
    )

    # ------------------------------------------------------------------ #
    # Razorpay Payment Gateway
    # ------------------------------------------------------------------ #
    RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "").strip()
    RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "").strip()
    RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET", "").strip()
    RAZORPAY_CURRENCY = os.getenv("RAZORPAY_CURRENCY", "INR").strip().upper()
    RAZORPAY_MODE = os.getenv("RAZORPAY_MODE", "test").strip().lower()

    @classmethod
    def is_razorpay_configured(cls) -> bool:
        """Return True if Razorpay key ID and secret are set."""
        return bool(cls.RAZORPAY_KEY_ID and cls.RAZORPAY_KEY_SECRET)

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


if Config.IS_PRODUCTION:
    _required_production_vars = (
        "DATABASE_URL",
        "SECRET_KEY",
        "JWT_SECRET_KEY",
        "FRONTEND_URL",
        "RAZORPAY_KEY_ID",
        "RAZORPAY_KEY_SECRET",
        "RAZORPAY_WEBHOOK_SECRET",
    )
    _missing_production_vars = [
        name for name in _required_production_vars if not os.getenv(name, "").strip()
    ]
    if _missing_production_vars:
        raise RuntimeError(
            "Missing required production environment variables: "
            + ", ".join(_missing_production_vars)
        )
    if Config.SECRET_KEY == "dev-secret-key-change-in-production":
        raise RuntimeError("SECRET_KEY must be changed from the development default in production.")
    if not Config.FRONTEND_URL.startswith("https://"):
        raise RuntimeError("FRONTEND_URL must be an HTTPS origin in production.")
    if any(
        origin == "*" or not origin.startswith("https://")
        for origin in Config.CORS_ALLOWED_ORIGINS
    ):
        raise RuntimeError("CORS_ALLOWED_ORIGINS must contain only HTTPS origins in production.")
