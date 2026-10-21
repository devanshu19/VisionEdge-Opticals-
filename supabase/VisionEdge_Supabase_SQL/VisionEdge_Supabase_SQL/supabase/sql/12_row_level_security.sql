-- Security baseline for tables in public schema.
-- Enabling RLS with no policies blocks anon/authenticated Data API access by default.
-- A backend PostgreSQL connection using a table-owner/BYPASSRLS role may bypass RLS;
-- do not treat RLS as a replacement for Flask authorization. Verify the actual DB role.
-- Run this only after reviewing the architecture and ensuring your app's DB role is
-- allowed to perform the operations it needs. This does not FORCE RLS on the owner.
ALTER TABLE public."user" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.customer ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.customer_profile ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.appointment ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.eye_test ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.prescription ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.frame ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.lens ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.supplier ENABLE ROW LEVEL SECURITY;
ALTER TABLE public."order" ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.order_item ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.billing ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.payment ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.lens_recommendation ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.frame_recommendation ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.virtual_try_on_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notification ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.brand ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.category ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.inventory_transaction ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.order_status_history ENABLE ROW LEVEL SECURITY;
