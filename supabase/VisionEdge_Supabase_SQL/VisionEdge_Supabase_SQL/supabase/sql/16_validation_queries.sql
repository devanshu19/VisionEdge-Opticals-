-- READ ONLY validation. Execute after the preceding schema files.
-- 1) Required table existence
SELECT expected.table_name,
       (to_regclass('public.' || quote_ident(expected.table_name)) IS NOT NULL) AS exists
FROM (VALUES
 ('user'),('customer'),('customer_profile'),('appointment'),('eye_test'),('prescription'),
 ('frame'),('lens'),('supplier'),('order'),('order_item'),('billing'),('payment'),
 ('lens_recommendation'),('frame_recommendation'),('virtual_try_on_history'),('chat_history'),
 ('notification'),('audit_log'),('brand'),('category'),('inventory_transaction'),('order_status_history')
) AS expected(table_name)
ORDER BY expected.table_name;

-- 2) Columns and data types
SELECT table_name, column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema='public' AND table_name IN (
 'user','customer','customer_profile','appointment','eye_test','prescription','frame','lens',
 'supplier','order','order_item','billing','payment','lens_recommendation','frame_recommendation',
 'virtual_try_on_history','chat_history','notification','audit_log','brand','category',
 'inventory_transaction','order_status_history')
ORDER BY table_name, ordinal_position;

-- 3) Primary keys and foreign keys
SELECT tc.table_name, tc.constraint_name, tc.constraint_type
FROM information_schema.table_constraints tc
WHERE tc.table_schema='public' AND tc.table_name IN (
 'user','customer','customer_profile','appointment','eye_test','prescription','frame','lens',
 'supplier','order','order_item','billing','payment','lens_recommendation','frame_recommendation',
 'virtual_try_on_history','chat_history','notification','audit_log','brand','category',
 'inventory_transaction','order_status_history')
ORDER BY tc.table_name, tc.constraint_type, tc.constraint_name;

-- 4) Indexes
SELECT schemaname, tablename, indexname, indexdef
FROM pg_indexes WHERE schemaname='public'
ORDER BY tablename, indexname;

-- 5) RLS status and policies
SELECT n.nspname AS schema_name, c.relname AS table_name, c.relrowsecurity AS rls_enabled,
       c.relforcerowsecurity AS force_rls
FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
WHERE n.nspname='public' AND c.relkind='r'
ORDER BY c.relname;
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual, with_check
FROM pg_policies WHERE schemaname='public' ORDER BY tablename, policyname;

-- 6) Trigger and function presence
SELECT event_object_table AS table_name, trigger_name, action_timing, event_manipulation
FROM information_schema.triggers WHERE trigger_schema='public' ORDER BY event_object_table, trigger_name;
SELECT n.nspname AS schema_name, p.proname AS function_name
FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
WHERE n.nspname='public' AND p.proname='visionedge_set_updated_at';

-- 7) Orphan checks (expected 0 after constraints are installed; no rows are modified)
SELECT 'customer_profile_without_customer' AS check_name, COUNT(*) AS issue_count
FROM public.customer_profile cp LEFT JOIN public.customer c ON c.id=cp.customer_id WHERE c.id IS NULL
UNION ALL
SELECT 'appointment_without_customer', COUNT(*) FROM public.appointment a LEFT JOIN public.customer c ON c.id=a.customer_id WHERE c.id IS NULL
UNION ALL
SELECT 'eye_test_without_customer', COUNT(*) FROM public.eye_test e LEFT JOIN public.customer c ON c.id=e.customer_id WHERE c.id IS NULL
UNION ALL
SELECT 'order_without_customer', COUNT(*) FROM public."order" o LEFT JOIN public.customer c ON c.id=o.customer_id WHERE c.id IS NULL
UNION ALL
SELECT 'order_item_without_order', COUNT(*) FROM public.order_item i LEFT JOIN public."order" o ON o.id=i.order_id WHERE o.id IS NULL
UNION ALL
SELECT 'billing_without_order', COUNT(*) FROM public.billing b LEFT JOIN public."order" o ON o.id=b.order_id WHERE o.id IS NULL
UNION ALL
SELECT 'payment_without_billing', COUNT(*) FROM public.payment p LEFT JOIN public.billing b ON b.id=p.billing_id WHERE b.id IS NULL;

-- 8) Row counts. These are observational counts, not proof of a data migration.
SELECT 'user' AS table_name, COUNT(*) AS row_count FROM public."user"
UNION ALL SELECT 'customer', COUNT(*) FROM public.customer
UNION ALL SELECT 'appointment', COUNT(*) FROM public.appointment
UNION ALL SELECT 'prescription', COUNT(*) FROM public.prescription
UNION ALL SELECT 'frame', COUNT(*) FROM public.frame
UNION ALL SELECT 'lens', COUNT(*) FROM public.lens
UNION ALL SELECT 'order', COUNT(*) FROM public."order"
UNION ALL SELECT 'billing', COUNT(*) FROM public.billing
UNION ALL SELECT 'payment', COUNT(*) FROM public.payment;
