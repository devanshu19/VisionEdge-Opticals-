-- VisionEdge / Supabase PostgreSQL setup
-- No extensions are required by the verified SQLAlchemy models.
-- Run in the intended Supabase project. This file is intentionally non-destructive.
SELECT current_database() AS database_name, current_user AS executing_role, version() AS postgres_version;
