import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3307")
    DB_NAME = os.getenv("DB_NAME", "visionedge_db")

    base_dir = os.path.abspath(os.path.dirname(__file__))
    sqlite_db_path = os.path.join(base_dir, 'visionedge.db')

    # Fallback to SQLite if USE_SQLITE is true
    use_sqlite = os.getenv("USE_SQLITE", "false").lower() == "true"

    if use_sqlite or not DB_PASSWORD:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{sqlite_db_path}"
    else:
        SQLALCHEMY_DATABASE_URI = os.getenv(
            "DATABASE_URL",
            f"mysql+pymysql://{quote_plus(DB_USER)}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False