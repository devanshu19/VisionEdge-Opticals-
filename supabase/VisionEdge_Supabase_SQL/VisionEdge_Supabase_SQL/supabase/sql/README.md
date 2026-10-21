# VisionEdge Supabase SQL setup (SQL-only deliverable)

These files were generated from the uploaded `VisionEdge/backend/models.py`, app setup, config, and route/helper source inspected in the ZIP. They are **not executed against Supabase** and do not migrate existing MySQL/SQLite data.

## Execution order

1. Create/open your Supabase project and open **SQL Editor → New query**.
2. Review and run `00_extensions_and_setup.sql`.
3. Run `01_enums_and_types.sql` through `09_indexes.sql` in numeric order.
4. Review `10_updated_at_triggers.sql`; run it if the updated-at triggers are wanted.
5. Review `11_functions_and_rpc.sql` (documentation only; no functions to run).
6. Review the security architecture before running `12_row_level_security.sql`. With no policies, RLS blocks normal Data API access to these tables. Do not run until you understand how Flask's database role connects and what it can bypass.
7. `13_rls_policies.sql` is conditional documentation only. Do not invent permissive policies.
8. `14_storage_setup_and_policies.sql` is conditional documentation only; current source uses local media paths, not Supabase Storage API.
9. `15_seed_reference_data.sql` intentionally inserts nothing.
10. Run `16_validation_queries.sql` after the schema files; it is read-only.
11. `17_optional_admin_bootstrap.sql` intentionally inserts no admin.

## File purpose

- `00_extensions_and_setup.sql`: connection/version confirmation; no extension required by inspected models.
- `01_enums_and_types.sql`: documents why status/role fields remain VARCHAR.
- `02_core_tables.sql`: user, customer, customer profile.
- `03_customer_and_eye_care_tables.sql`: appointment, eye test, prescription.
- `04_inventory_tables.sql`: brand/category/supplier/frame/lens/inventory transactions.
- `05_orders_billing_and_payments.sql`: order, items, billing, payments, order status history.
- `06_ai_and_recommendation_tables.sql`: AI recommendations, VTO, chat history.
- `07_notifications_audit_and_history.sql`: notifications and audit logs.
- `08_foreign_keys_and_constraints.sql`: foreign keys after all tables exist.
- `09_indexes.sql`: indexes aligned to route filters and relationships.
- `10_updated_at_triggers.sql`: customer/frame `updated_at` triggers.
- `11_functions_and_rpc.sql`: stock logic warning; no RPC installed.
- `12_row_level_security.sql`: conditional RLS enablement; review before running.
- `13_rls_policies.sql`: no policies until identity mapping is designed.
- `14_storage_setup_and_policies.sql`: Storage integration is not present in inspected source.
- `15_seed_reference_data.sql`: no inserts.
- `16_validation_queries.sql`: read-only checks.
- `17_optional_admin_bootstrap.sql`: no admin inserted.
- `QUERY_MIGRATION_INVENTORY.md`: route/helper audit and remaining compatibility work.

## Manual checklist

- [ ] Confirm this is the intended Supabase project and environment.
- [ ] Back up any existing target data before schema work.
- [ ] Run files `00`–`09` in order and inspect each result for errors.
- [ ] Review foreign keys and delete behavior before production use.
- [ ] Review and decide whether to run the RLS file; do not run blindly.
- [ ] Confirm Flask's configured database driver/URL and permissions separately.
- [ ] Run `16_validation_queries.sql` and inspect the output.
- [ ] Open **Table Editor** and confirm tables/columns; inspect relationships and indexes.
- [ ] Plan and authorize data migration separately; schema creation does not move existing data.
- [ ] Keep credentials and service-role keys out of SQL files and source control.

## Table Editor / error handling

In Supabase Dashboard, choose the project → **Table Editor** → `public` schema. Use the table details/relationship view to inspect foreign keys; use validation query 4 to inspect indexes. If a query errors, stop at that file, read the complete error, fix the cause, and rerun only after determining whether partial statements succeeded. Do not run destructive reset scripts to "fix" an error.

## Important compatibility limits

- Existing config supports SQLite fallback and MySQL/PyMySQL; the Python connection configuration has not been changed to PostgreSQL.
- `mysql_db.py` directly uses PyMySQL and `lastrowid`, which is MySQL-specific. Its callers and all query paths must be audited and updated before using PostgreSQL.
- `app.py` calls `db.create_all()` when run as a script. The current application may create tables independently; this SQL package is a manual alternative schema, not an instruction to run both systems blindly.
- Existing Flask JWT authorization is not automatically understood by Supabase RLS. Policies require a reviewed identity propagation strategy.
- Files are currently local paths served from `backend/media`; Storage SQL cannot move those files or alter upload/download code.
- Stock deductions and inventory transaction inserts happen in `backend/utils/signals.py`. Do not add a second stock trigger.
- The schema preserves the polymorphic inventory transaction product reference without a foreign key because it can refer to either frames or lenses.
- Financial fields are NUMERIC in PostgreSQL even though the model currently uses Python Float; review serialization/rounding behavior during the required backend migration.

**No SQL in this package has been run against a live database.**
