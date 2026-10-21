"""
migrate_to_supabase.py
======================
Safe, data-preserving migration utility.
Transfers records from the existing SQLite / MySQL source database
to the configured Supabase PostgreSQL target.

SAFETY CONTRACT
---------------
* Reads the SOURCE database without modifying or deleting any record.
* Dry-run mode (--dry-run) prints counts/plan without writing anything.
* Stops when a migration would lose or overwrite existing data.
* Does NOT seed sample records into production automatically.
* Does NOT expose password hashes in output or logs.
* Does NOT migrate local image files (separate task).

USAGE (from backend/ directory with venv activated)
-----------------------------------------------------
  # Dry-run — shows counts and plan:
  python migrate_to_supabase.py --dry-run

  # Migrate all tables:
  python migrate_to_supabase.py

  # Migrate specific tables:
  python migrate_to_supabase.py --tables user,customer,frame,lens

  # Specify a custom source URI:
  python migrate_to_supabase.py --source "sqlite:///visionedge.db"

PREREQUISITES
-------------
  DATABASE_URL must point to the Supabase PostgreSQL target.
  SOURCE_DATABASE_URL (optional) can override the source.
  pip install psycopg2-binary sqlalchemy pymysql python-dotenv
"""

import argparse
import os
import sys
from datetime import datetime

# Ensure backend/ is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

# Table migration order respects FK dependencies
MIGRATION_ORDER = [
    "user",
    "customer",
    "customer_profile",
    "supplier",
    "brand",
    "category",
    "frame",
    "lens",
    "appointment",
    "eye_test",
    "prescription",
    "order",
    "order_item",
    "billing",
    "payment",
    "order_status_history",
    "inventory_transaction",
    "lens_recommendation",
    "frame_recommendation",
    "virtual_try_on_history",
    "chat_history",
    "notification",
    "audit_log",
]

BATCH_SIZE = 200  # rows per insert batch


def get_source_engine():
    """Build the source SQLAlchemy engine."""
    from sqlalchemy import create_engine
    source_uri = os.getenv("SOURCE_DATABASE_URL", "").strip()
    if not source_uri:
        # Default to local SQLite
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sqlite_path = os.path.join(base_dir, "visionedge.db")
        if not os.path.exists(sqlite_path):
            print(f"[ERROR] Source SQLite not found: {sqlite_path}")
            print("        Set SOURCE_DATABASE_URL to specify a different source.")
            sys.exit(1)
        source_uri = f"sqlite:///{sqlite_path}"
        print(f"[SOURCE] Using local SQLite: {sqlite_path}")
    else:
        # Mask credentials in log
        from urllib.parse import urlparse
        p = urlparse(source_uri)
        print(f"[SOURCE] {p.scheme}://{p.host}:{p.port}/{p.path.lstrip('/')}")
    return create_engine(source_uri, pool_pre_ping=True)


def get_target_engine():
    """Build the target Supabase PostgreSQL SQLAlchemy engine."""
    from sqlalchemy import create_engine
    from urllib.parse import urlparse

    target_uri = os.getenv("DATABASE_URL", "").strip() or os.getenv("SUPABASE_DB_URL", "").strip()
    if not target_uri:
        print("[ERROR] DATABASE_URL is not set. Cannot connect to Supabase.")
        print("        Set DATABASE_URL to your Supabase PostgreSQL connection string.")
        sys.exit(1)

    # Normalise postgres:// → postgresql+psycopg2://
    if target_uri.startswith("postgres://"):
        target_uri = "postgresql+psycopg2://" + target_uri[len("postgres://"):]
    elif target_uri.startswith("postgresql://") and "+psycopg" not in target_uri:
        target_uri = target_uri.replace("postgresql://", "postgresql+psycopg2://", 1)

    p = urlparse(target_uri)
    print(f"[TARGET] {p.scheme.split('+')[0]}://{p.host}:{p.port}/{p.path.lstrip('/')}")
    return create_engine(target_uri, pool_pre_ping=True, connect_args={"sslmode": "require"})


def get_tables(engine, requested: list[str] | None) -> list[str]:
    """Return the intersection of requested tables and actually-existing tables."""
    from sqlalchemy import inspect
    insp = inspect(engine)
    existing = set(insp.get_table_names())
    if requested:
        missing = [t for t in requested if t not in existing]
        if missing:
            print(f"[WARN] These requested tables don't exist in source: {missing}")
        return [t for t in MIGRATION_ORDER if t in existing and t in requested]
    return [t for t in MIGRATION_ORDER if t in existing]


def count_rows(conn, table_name: str) -> int:
    from sqlalchemy import text
    result = conn.execute(text(f"SELECT COUNT(*) FROM \"{table_name}\""))
    return result.scalar()


def migrate_table(src_conn, tgt_conn, table_name: str, dry_run: bool) -> dict:
    """Migrate a single table. Returns a result dict."""
    from sqlalchemy import text, MetaData, Table

    src_meta = MetaData()
    src_meta.reflect(bind=src_conn.engine, only=[table_name])
    if table_name not in src_meta.tables:
        return {"table": table_name, "status": "SKIPPED", "source": 0, "migrated": 0}

    src_table = src_meta.tables[table_name]

    src_count = count_rows(src_conn, table_name)
    print(f"  [{table_name}] Source rows: {src_count}", end="", flush=True)

    if dry_run:
        print(f"  → DRY RUN, skipping insert.")
        return {"table": table_name, "status": "DRY_RUN", "source": src_count, "migrated": 0}

    # Check how many rows already exist in target (safe rerun)
    try:
        existing_count = count_rows(tgt_conn, table_name)
    except Exception:
        existing_count = 0

    if existing_count > 0:
        print(f"  → Target already has {existing_count} rows — SKIPPING (re-run safe).")
        return {"table": table_name, "status": "SKIPPED_EXISTING", "source": src_count, "migrated": 0}

    # Stream source in batches
    migrated = 0
    failed = 0
    offset = 0
    columns = [c.name for c in src_table.columns]

    while offset < src_count:
        rows = src_conn.execute(
            text(f"SELECT * FROM \"{table_name}\" LIMIT {BATCH_SIZE} OFFSET {offset}")
        ).mappings().all()

        if not rows:
            break

        batch = []
        for row in rows:
            record = {}
            for col in columns:
                val = row[col]
                # Normalise None / null correctly
                record[col] = val
            batch.append(record)

        try:
            tgt_meta = MetaData()
            tgt_meta.reflect(bind=tgt_conn.engine, only=[table_name])
            if table_name in tgt_meta.tables:
                tgt_conn.execute(tgt_meta.tables[table_name].insert(), batch)
                tgt_conn.commit()
                migrated += len(batch)
        except Exception as e:
            failed += len(batch)
            # Log failure type without printing sensitive row content
            print(f"\n  [ERROR] Batch failed at offset {offset}: {type(e).__name__}: {e}")
            tgt_conn.rollback()

        offset += BATCH_SIZE
        print(".", end="", flush=True)

    print(f"  → Migrated: {migrated}, Failed: {failed}")
    status = "OK" if failed == 0 else "PARTIAL"
    return {"table": table_name, "status": status, "source": src_count, "migrated": migrated}


def reset_sequences(tgt_conn, table_names: list[str]):
    """
    For PostgreSQL: reset sequences after migrating rows with explicit IDs.
    This prevents primary-key conflicts on future inserts.
    """
    from sqlalchemy import text
    print("\n[SEQUENCES] Resetting PostgreSQL sequences...")
    for table in table_names:
        try:
            tgt_conn.execute(text(
                f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), "
                f"COALESCE(MAX(id), 0) + 1, false) FROM \"{table}\""
            ))
            tgt_conn.commit()
            print(f"  [{table}] sequence reset OK")
        except Exception as e:
            print(f"  [{table}] sequence reset skipped: {type(e).__name__}")


def print_report(results: list[dict]):
    print("\n" + "=" * 60)
    print("MIGRATION RECONCILIATION REPORT")
    print("=" * 60)
    print(f"{'Table':<35} {'Status':<18} {'Source':>8} {'Migrated':>9}")
    print("-" * 60)
    for r in results:
        print(f"{r['table']:<35} {r['status']:<18} {r['source']:>8} {r['migrated']:>9}")
    print("=" * 60)
    total_src = sum(r['source'] for r in results)
    total_mig = sum(r['migrated'] for r in results)
    print(f"{'TOTAL':<35} {'':<18} {total_src:>8} {total_mig:>9}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Migrate VisionEdge data from SQLite/MySQL to Supabase PostgreSQL."
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Print plan and counts only; do not write to target.")
    parser.add_argument("--tables", type=str, default=None,
                        help="Comma-separated list of tables to migrate (default: all).")
    parser.add_argument("--source", type=str, default=None,
                        help="Override source DATABASE URI.")
    args = parser.parse_args()

    if args.source:
        os.environ["SOURCE_DATABASE_URL"] = args.source

    requested = [t.strip() for t in args.tables.split(",")] if args.tables else None

    print(f"\n{'=' * 60}")
    print(f"VisionEdge → Supabase Migration  [{datetime.utcnow().isoformat()} UTC]")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"{'=' * 60}\n")

    src_engine = get_source_engine()
    tgt_engine = get_target_engine()

    with src_engine.connect() as src_conn, tgt_engine.connect() as tgt_conn:
        tables = get_tables(src_conn.engine, requested)

        print(f"\n[PLAN] Tables to migrate ({len(tables)}):")
        for t in tables:
            print(f"  - {t}")
        print()

        results = []
        for table in tables:
            print(f"\n[TABLE] {table}")
            result = migrate_table(src_conn, tgt_conn, table, args.dry_run)
            results.append(result)

        if not args.dry_run:
            reset_sequences(tgt_conn, [r["table"] for r in results if r["status"] == "OK"])

    print_report(results)

    # Exit with error if any table failed
    if any(r["status"] == "PARTIAL" for r in results):
        print("[WARN] Some tables had partial failures. Review errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
