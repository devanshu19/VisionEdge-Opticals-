-- Add foreign keys after all referenced tables exist. DO blocks make this file repeatable
-- when the named constraint already exists; no data is changed.
DO $$ BEGIN
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_customer_created_by') THEN
  ALTER TABLE public.customer ADD CONSTRAINT fk_customer_created_by FOREIGN KEY (created_by) REFERENCES public."user"(id) ON DELETE SET NULL;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_customer_profile_customer') THEN
  ALTER TABLE public.customer_profile ADD CONSTRAINT fk_customer_profile_customer FOREIGN KEY (customer_id) REFERENCES public.customer(id) ON DELETE CASCADE;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_appointment_customer') THEN
  ALTER TABLE public.appointment ADD CONSTRAINT fk_appointment_customer FOREIGN KEY (customer_id) REFERENCES public.customer(id) ON DELETE CASCADE;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_eye_test_customer') THEN
  ALTER TABLE public.eye_test ADD CONSTRAINT fk_eye_test_customer FOREIGN KEY (customer_id) REFERENCES public.customer(id) ON DELETE CASCADE;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_eye_test_appointment') THEN
  ALTER TABLE public.eye_test ADD CONSTRAINT fk_eye_test_appointment FOREIGN KEY (appointment_id) REFERENCES public.appointment(id) ON DELETE SET NULL;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_prescription_customer') THEN
  ALTER TABLE public.prescription ADD CONSTRAINT fk_prescription_customer FOREIGN KEY (customer_id) REFERENCES public.customer(id) ON DELETE CASCADE;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_prescription_eye_test') THEN
  ALTER TABLE public.prescription ADD CONSTRAINT fk_prescription_eye_test FOREIGN KEY (eye_test_id) REFERENCES public.eye_test(id) ON DELETE SET NULL;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_order_customer') THEN
  ALTER TABLE public."order" ADD CONSTRAINT fk_order_customer FOREIGN KEY (customer_id) REFERENCES public.customer(id) ON DELETE RESTRICT;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_order_prescription') THEN
  ALTER TABLE public."order" ADD CONSTRAINT fk_order_prescription FOREIGN KEY (prescription_id) REFERENCES public.prescription(id) ON DELETE SET NULL;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_order_item_order') THEN
  ALTER TABLE public.order_item ADD CONSTRAINT fk_order_item_order FOREIGN KEY (order_id) REFERENCES public."order"(id) ON DELETE CASCADE;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_billing_order') THEN
  ALTER TABLE public.billing ADD CONSTRAINT fk_billing_order FOREIGN KEY (order_id) REFERENCES public."order"(id) ON DELETE RESTRICT;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_payment_billing') THEN
  ALTER TABLE public.payment ADD CONSTRAINT fk_payment_billing FOREIGN KEY (billing_id) REFERENCES public.billing(id) ON DELETE CASCADE;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_order_status_history_order') THEN
  ALTER TABLE public.order_status_history ADD CONSTRAINT fk_order_status_history_order FOREIGN KEY (order_id) REFERENCES public."order"(id) ON DELETE CASCADE;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_lens_recommendation_customer') THEN
  ALTER TABLE public.lens_recommendation ADD CONSTRAINT fk_lens_recommendation_customer FOREIGN KEY (customer_id) REFERENCES public.customer(id) ON DELETE SET NULL;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_lens_recommendation_prescription') THEN
  ALTER TABLE public.lens_recommendation ADD CONSTRAINT fk_lens_recommendation_prescription FOREIGN KEY (prescription_id) REFERENCES public.prescription(id) ON DELETE SET NULL;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_frame_recommendation_customer') THEN
  ALTER TABLE public.frame_recommendation ADD CONSTRAINT fk_frame_recommendation_customer FOREIGN KEY (customer_id) REFERENCES public.customer(id) ON DELETE CASCADE;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_vto_customer') THEN
  ALTER TABLE public.virtual_try_on_history ADD CONSTRAINT fk_vto_customer FOREIGN KEY (customer_id) REFERENCES public.customer(id) ON DELETE CASCADE;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_vto_frame') THEN
  ALTER TABLE public.virtual_try_on_history ADD CONSTRAINT fk_vto_frame FOREIGN KEY (frame_id) REFERENCES public.frame(id) ON DELETE RESTRICT;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_chat_user') THEN
  ALTER TABLE public.chat_history ADD CONSTRAINT fk_chat_user FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE SET NULL;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_chat_customer') THEN
  ALTER TABLE public.chat_history ADD CONSTRAINT fk_chat_customer FOREIGN KEY (customer_id) REFERENCES public.customer(id) ON DELETE SET NULL;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_notification_user') THEN
  ALTER TABLE public.notification ADD CONSTRAINT fk_notification_user FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE SET NULL;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_notification_customer') THEN
  ALTER TABLE public.notification ADD CONSTRAINT fk_notification_customer FOREIGN KEY (customer_id) REFERENCES public.customer(id) ON DELETE CASCADE;
 END IF;
 IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='fk_audit_log_user') THEN
  ALTER TABLE public.audit_log ADD CONSTRAINT fk_audit_log_user FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE SET NULL;
 END IF;
END $$;
-- Polymorphic inventory_transaction.product_id intentionally has no FK: it can refer
-- to either frame.id or lens.id, and the source model does not encode a single target.
