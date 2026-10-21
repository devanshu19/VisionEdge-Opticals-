-- Keep updated_at current for models that define SQLAlchemy onupdate behavior.
CREATE OR REPLACE FUNCTION public.visionedge_set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;
DROP TRIGGER IF EXISTS trg_customer_updated_at ON public.customer;
CREATE TRIGGER trg_customer_updated_at BEFORE UPDATE ON public.customer
FOR EACH ROW EXECUTE FUNCTION public.visionedge_set_updated_at();
DROP TRIGGER IF EXISTS trg_frame_updated_at ON public.frame;
CREATE TRIGGER trg_frame_updated_at BEFORE UPDATE ON public.frame
FOR EACH ROW EXECUTE FUNCTION public.visionedge_set_updated_at();
-- No trigger is created for lens because its source model has no updated_at column.
