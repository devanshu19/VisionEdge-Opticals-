"""
VisionEdge — Database Migration for Razorpay Payment Gateway & Webhook Events
=============================================================================
Supports:
  - Supabase PostgreSQL (Production / Cloud)
  - SQLite (Local Dev / Offline Tests)
"""

import sys
import os
from sqlalchemy import text, inspect

# Ensure backend directory is in sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app import create_app
from models import db


def migrate():
    app = create_app()
    with app.app_context():
        dialect = db.engine.dialect.name
        print(f"[*] Starting Razorpay database migration on [{dialect}] database...")

        inspector = inspect(db.engine)
        table_names = inspector.get_table_names()

        # -------------------------------------------------------------
        # 1. Migrate `payment` table
        # -------------------------------------------------------------
        if "payment" not in table_names:
            print("[!] Table 'payment' not found. Creating all tables via db.create_all()...")
            db.create_all()
            print("[+] Tables created successfully.")
            return

        existing_columns = {col["name"] for col in inspector.get_columns("payment")}
        print(f"[*] Existing 'payment' table columns ({len(existing_columns)}): {existing_columns}")

        columns_to_add = [
            ("order_id", "INTEGER", "order_id INTEGER REFERENCES \"order\"(id)" if dialect == "postgresql" else "order_id INTEGER"),
            ("currency", "VARCHAR(10)", "currency VARCHAR(10) DEFAULT 'INR'"),
            ("gateway", "VARCHAR(50)", "gateway VARCHAR(50) DEFAULT 'Razorpay'"),
            ("gateway_order_id", "VARCHAR(100)", "gateway_order_id VARCHAR(100)"),
            ("gateway_payment_id", "VARCHAR(100)", "gateway_payment_id VARCHAR(100)"),
            ("gateway_signature", "VARCHAR(255)", "gateway_signature VARCHAR(255)"),
            ("gateway_status", "VARCHAR(50)", "gateway_status VARCHAR(50) DEFAULT 'created'"),
            ("signature_verified", "BOOLEAN", "signature_verified BOOLEAN DEFAULT FALSE" if dialect == "postgresql" else "signature_verified BOOLEAN DEFAULT 0"),
            ("failure_code", "VARCHAR(100)", "failure_code VARCHAR(100)"),
            ("failure_reason", "TEXT", "failure_reason TEXT"),
            ("refund_status", "VARCHAR(50)", "refund_status VARCHAR(50)"),
            ("refunded_amount", "NUMERIC(12,2)" if dialect == "postgresql" else "FLOAT", "refunded_amount NUMERIC(12,2) DEFAULT 0.00" if dialect == "postgresql" else "refunded_amount FLOAT DEFAULT 0.0"),
            ("refund_id", "VARCHAR(100)", "refund_id VARCHAR(100)"),
            ("raw_response", "TEXT", "raw_response TEXT"),
            ("created_at", "TIMESTAMP" if dialect == "postgresql" else "DATETIME", "created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP" if dialect == "postgresql" else "created_at DATETIME DEFAULT CURRENT_TIMESTAMP"),
            ("updated_at", "TIMESTAMP" if dialect == "postgresql" else "DATETIME", "updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP" if dialect == "postgresql" else "updated_at DATETIME DEFAULT CURRENT_TIMESTAMP"),
            ("paid_at", "TIMESTAMP" if dialect == "postgresql" else "DATETIME", "paid_at TIMESTAMP WITHOUT TIME ZONE" if dialect == "postgresql" else "paid_at DATETIME"),
        ]

        with db.engine.connect() as conn:
            for col_name, col_type, col_def in columns_to_add:
                if col_name not in existing_columns:
                    print(f"[*] Adding column '{col_name}' to 'payment' table...")
                    alter_sql = f"ALTER TABLE payment ADD COLUMN {col_def};"
                    try:
                        conn.execute(text(alter_sql))
                        print(f"    [+] Added '{col_name}'.")
                    except Exception as e:
                        print(f"    [-] Warning adding '{col_name}': {e}")
                else:
                    print(f"    [~] Column '{col_name}' already exists in 'payment'.")

            # ---------------------------------------------------------
            # 2. Indexes on `payment`
            # ---------------------------------------------------------
            print("[*] Ensuring indexes on 'payment'...")
            index_sqls = []
            if dialect == "postgresql":
                index_sqls = [
                    "CREATE UNIQUE INDEX IF NOT EXISTS uq_payment_gateway_payment_id ON public.payment(gateway_payment_id) WHERE gateway_payment_id IS NOT NULL;",
                    "CREATE INDEX IF NOT EXISTS idx_payment_gateway_order_id ON public.payment(gateway_order_id);",
                    "CREATE INDEX IF NOT EXISTS idx_payment_order_id ON public.payment(order_id);"
                ]
            else:
                index_sqls = [
                    "CREATE INDEX IF NOT EXISTS idx_payment_gateway_order_id ON payment(gateway_order_id);",
                    "CREATE INDEX IF NOT EXISTS idx_payment_gateway_payment_id ON payment(gateway_payment_id);",
                    "CREATE INDEX IF NOT EXISTS idx_payment_order_id ON payment(order_id);"
                ]

            for idx_sql in index_sqls:
                try:
                    conn.execute(text(idx_sql))
                except Exception as e:
                    print(f"    [-] Warning creating index ({idx_sql}): {e}")
            print("    [+] Indexes created or verified.")

            # ---------------------------------------------------------
            # 3. Create `webhook_event` table
            # ---------------------------------------------------------
            print("[*] Checking 'webhook_event' table...")
            if "webhook_event" not in table_names:
                print("[*] Creating 'webhook_event' table...")
                if dialect == "postgresql":
                    create_tbl_sql = """
                        CREATE TABLE IF NOT EXISTS public.webhook_event (
                            id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                            gateway VARCHAR(50) NOT NULL DEFAULT 'Razorpay',
                            event_id VARCHAR(100) NOT NULL UNIQUE,
                            event_type VARCHAR(100) NOT NULL,
                            payload TEXT,
                            status VARCHAR(50) NOT NULL DEFAULT 'pending',
                            error_message TEXT,
                            received_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                            processed_at TIMESTAMP WITHOUT TIME ZONE
                        );
                    """
                    idx_sqls = [
                        "CREATE INDEX IF NOT EXISTS idx_webhook_event_id ON public.webhook_event(event_id);",
                        "CREATE INDEX IF NOT EXISTS idx_webhook_event_status ON public.webhook_event(status);"
                    ]
                else:
                    create_tbl_sql = """
                        CREATE TABLE IF NOT EXISTS webhook_event (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            gateway VARCHAR(50) NOT NULL DEFAULT 'Razorpay',
                            event_id VARCHAR(100) NOT NULL UNIQUE,
                            event_type VARCHAR(100) NOT NULL,
                            payload TEXT,
                            status VARCHAR(50) NOT NULL DEFAULT 'pending',
                            error_message TEXT,
                            received_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                            processed_at DATETIME
                        );
                    """
                    idx_sqls = [
                        "CREATE INDEX IF NOT EXISTS idx_webhook_event_id ON webhook_event(event_id);",
                        "CREATE INDEX IF NOT EXISTS idx_webhook_event_status ON webhook_event(status);"
                    ]

                conn.execute(text(create_tbl_sql))
                for isql in idx_sqls:
                    conn.execute(text(isql))
                print("    [+] 'webhook_event' table and indexes created.")
            else:
                print("    [~] 'webhook_event' table already exists.")

            conn.commit()

        print("[SUCCESS] Razorpay database migration finished successfully!")


if __name__ == "__main__":
    migrate()
