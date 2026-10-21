-- =============================================================================
-- FILE: 00_extensions_and_setup.sql
-- PURPOSE: Enable required PostgreSQL extensions for VisionEdge.
-- EXECUTE: First. Run once per Supabase project.
-- SAFE TO RERUN: Yes (CREATE EXTENSION IF NOT EXISTS is idempotent).
-- =============================================================================

-- pgcrypto: Used for gen_random_uuid() and cryptographic functions.
-- Required by Supabase by default; explicitly enabled here for clarity.
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- uuid-ossp: Provides uuid_generate_v4(). Supabase includes this by default.
-- Listed here in case a fallback is needed.
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- pg_trgm: Enables trigram-based fuzzy text search (ILIKE optimisation).
-- Used for customer search, frame/lens search in the inventory routes.
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- unaccent: Enables accent-insensitive text search.
-- Useful for customer name searches across Indian regional name variants.
CREATE EXTENSION IF NOT EXISTS "unaccent";

-- =============================================================================
-- DATABASE ROLE NOTE
-- =============================================================================
-- VisionEdge uses Flask-SQLAlchemy as the only data-access layer.
-- The browser NEVER connects directly to PostgreSQL.
-- Flask connects using the DATABASE_URL credential (typically the
-- 'postgres' role or a dedicated application role you create in Supabase).
--
-- If you create a dedicated app role, grant it the minimum required:
--   CREATE ROLE visionedge_app LOGIN PASSWORD 'strong_password';
--   GRANT CONNECT ON DATABASE postgres TO visionedge_app;
--   GRANT USAGE ON SCHEMA public TO visionedge_app;
--   GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO visionedge_app;
--   GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO visionedge_app;
--   ALTER DEFAULT PRIVILEGES IN SCHEMA public
--     GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO visionedge_app;
--   ALTER DEFAULT PRIVILEGES IN SCHEMA public
--     GRANT USAGE, SELECT ON SEQUENCES TO visionedge_app;
--
-- The above is optional for initial setup. You can use the default
-- Supabase postgres role while developing.
-- =============================================================================

-- Ensure the public schema is set correctly
SET search_path TO public;
