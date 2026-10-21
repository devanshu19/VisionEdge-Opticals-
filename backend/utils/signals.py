from sqlalchemy import event, text
from models import Frame, Lens, Order, OrderItem, Billing, Appointment
from utils.services import create_notification
from datetime import datetime


def register_signals():
    """
    Registers SQLAlchemy event listeners to automate notification creation.
    Must be called inside the app context on startup.

    IMPORTANT: These listeners execute during the SQLAlchemy flush phase using
    the low-level `connection` object (not db.session).  Raw SQL here must be
    PostgreSQL-compatible:
      - CURRENT_TIMESTAMP is standard SQL and works on all backends.
      - Column names must match the actual table columns (product_type / product_id).
      - Named bind parameters (:name) are used — no MySQL %s or SQLite ? placeholders.
    """

    # ------------------------------------------------------------------ #
    # 1. LOW STOCK ALERTS
    # ------------------------------------------------------------------ #
    def check_low_stock(mapper, connection, target):
        if target.stock <= target.min_stock:
            create_notification(
                notification_type='LOW_STOCK',
                title='Low Stock Alert',
                message=(
                    f"{target.name} stock has dropped to {target.stock} units. "
                    f"(Min required: {target.min_stock})"
                )
            )

    event.listen(Frame, 'after_update', check_low_stock)
    event.listen(Lens, 'after_update', check_low_stock)

    # ------------------------------------------------------------------ #
    # 2. NEW ORDER & ORDER STATUS
    # ------------------------------------------------------------------ #
    def on_order_insert(mapper, connection, target):
        create_notification(
            notification_type='NEW_ORDER',
            title='New Order Received',
            message=f"Order {target.order_number} has been created for Customer {target.customer_id}."
        )

    def on_order_item_insert(mapper, connection, target):
        """
        Deduct stock and log inventory transaction when an OrderItem is inserted.

        Uses the canonical column names (product_type / product_id) that exist
        in the inventory_transaction table, with a fallback to aliases
        (item_type / item_id) that older table versions may have had.

        The raw SQL is PostgreSQL-safe:
          - Named parameters :name with text() construct.
          - CURRENT_TIMESTAMP is ANSI SQL.
          - No backtick quoting.
        """
        # Resolve the effective item type and id
        itype = getattr(target, 'product_type', None) or getattr(target, 'item_type', None)
        iid   = getattr(target, 'product_id',   None) or getattr(target, 'item_id',   None)

        if not itype or not iid:
            return

        # Deduct stock
        if itype == 'Frame':
            connection.execute(
                text("UPDATE frame SET stock = stock - :qty WHERE id = :id"),
                {"qty": target.quantity, "id": iid}
            )
        elif itype == 'Lens':
            connection.execute(
                text("UPDATE lens SET stock = stock - :qty WHERE id = :id"),
                {"qty": target.quantity, "id": iid}
            )

        # Log Inventory Transaction using canonical column names
        try:
            connection.execute(
                text("""
                    INSERT INTO inventory_transaction
                        (product_type, product_id, transaction_type, quantity,
                         notes, created_at)
                    VALUES (:itype, :iid, 'Sale', :qty, :notes, CURRENT_TIMESTAMP)
                """),
                {
                    "itype": itype,
                    "iid": iid,
                    "qty": target.quantity,
                    "notes": f"Order item sale (Order ID: {target.order_id})"
                }
            )
        except Exception:
            # Don't let inventory logging failure break order creation
            pass

    def on_order_update(mapper, connection, target):
        if target.status == 'Ready for Pickup':
            create_notification(
                notification_type='ORDER_READY',
                title='Order Ready',
                message=f"Your order {target.order_number} is ready for pickup.",
                customer_id=target.customer_id
            )
        elif target.status == 'Delivered':
            create_notification(
                notification_type='ORDER_COMPLETED',
                title='Order Completed',
                message=(
                    f"Thank you for shopping with VisionEdge. "
                    f"Order {target.order_number} is completed."
                ),
                customer_id=target.customer_id
            )

    event.listen(Order, 'after_insert', on_order_insert)
    event.listen(OrderItem, 'after_insert', on_order_item_insert)
    event.listen(Order, 'after_update', on_order_update)

    # ------------------------------------------------------------------ #
    # 3. PAYMENT PENDING ALERTS
    # ------------------------------------------------------------------ #
    def on_billing_insert(mapper, connection, target):
        if target.payment_status == 'Pending':
            create_notification(
                notification_type='PAYMENT_PENDING',
                title='Pending Payment',
                message=(
                    f"Pending payment for invoice {target.invoice_number}. "
                    f"Total: \u20b9{target.total_amount}."
                ),
                customer_id=None
            )

    def on_billing_update(mapper, connection, target):
        if target.payment_status == 'Pending':
            create_notification(
                notification_type='PAYMENT_PENDING',
                title='Pending Payment',
                message=(
                    f"Pending payment for invoice {target.invoice_number}. "
                    f"Total: \u20b9{target.total_amount}."
                ),
                customer_id=None
            )

    event.listen(Billing, 'after_insert', on_billing_insert)
    event.listen(Billing, 'after_update', on_billing_update)

    # ------------------------------------------------------------------ #
    # 4. APPOINTMENT REMINDER
    # ------------------------------------------------------------------ #
    def on_appointment_insert(mapper, connection, target):
        if target.status == 'Pending':
            dt = (
                datetime.combine(target.appointment_date, target.appointment_time)
                if target.appointment_date and target.appointment_time
                else datetime.utcnow()
            )
            create_notification(
                notification_type='APPOINTMENT_REMINDER',
                title='Appointment Reminder',
                message=(
                    f"Reminder: Your eye test appointment is scheduled on "
                    f"{dt.strftime('%Y-%m-%d %I:%M %p')}."
                ),
                customer_id=target.customer_id
            )

    event.listen(Appointment, 'after_insert', on_appointment_insert)
