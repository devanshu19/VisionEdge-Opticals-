from sqlalchemy import event
from models import Frame, Lens, Order, OrderItem, Billing, Appointment
from utils.services import create_notification
from datetime import datetime

def register_signals():
    """
    Registers SQLAlchemy event listeners to automate notification creation.
    Must be called inside the app context on startup.
    """
    
    # 1. LOW STOCK ALERTS
    def check_low_stock(mapper, connection, target):
        if target.stock <= target.min_stock:
            create_notification(
                notification_type='LOW_STOCK',
                title='Low Stock Alert',
                message=f"{target.name} stock has dropped to {target.stock} units. (Min required: {target.min_stock})"
            )

    event.listen(Frame, 'after_update', check_low_stock)
    event.listen(Lens, 'after_update', check_low_stock)

    # 2. NEW ORDER & ORDER STATUS
    def on_order_insert(mapper, connection, target):
        create_notification(
            notification_type='NEW_ORDER',
            title='New Order Received',
            message=f"Order {target.order_number} has been created for Customer {target.customer_id}."
        )

    def on_order_item_insert(mapper, connection, target):
        from sqlalchemy import text

        # Resolve field names — OrderItem uses item_type / item_id
        itype = getattr(target, 'item_type', None) or getattr(target, 'product_type', None)
        iid   = getattr(target, 'item_id',   None) or getattr(target, 'product_id',   None)

        if not itype or not iid:
            return

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

        # Log Inventory Transaction — try both column name schemas gracefully
        try:
            connection.execute(
                text("""
                    INSERT INTO inventory_transaction
                        (item_type, item_id, transaction_type, quantity, reason, created_at)
                    VALUES (:itype, :iid, 'Sale', :qty, :reason, CURRENT_TIMESTAMP)
                """),
                {
                    "itype": itype,
                    "iid": iid,
                    "qty": target.quantity,
                    "reason": f"Order item sale (Order ID: {target.order_id})"
                }
            )
        except Exception:
            try:
                connection.execute(
                    text("""
                        INSERT INTO inventory_transaction
                            (product_type, product_id, transaction_type, quantity, notes, created_at)
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
                pass  # Don't let logging failure break the order

    def on_order_update(mapper, connection, target):
        # We check state changes in a real app by inspecting session, 
        # but for simplicity, we trigger on specific statuses.
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
                message=f"Thank you for shopping with VisionEdge. Order {target.order_number} is completed.",
                customer_id=target.customer_id
            )

    event.listen(Order, 'after_insert', on_order_insert)
    event.listen(OrderItem, 'after_insert', on_order_item_insert)
    event.listen(Order, 'after_update', on_order_update)

    # 3. PAYMENT PENDING ALERTS
    def on_billing_insert(mapper, connection, target):
        if target.payment_status == 'Pending':
            create_notification(
                notification_type='PAYMENT_PENDING',
                title='Pending Payment',
                message=f"Pending payment for invoice {target.invoice_number}. Total: ₹{target.total_amount}.",
                customer_id=None # We omit customer_id here to avoid querying inside flush, admins still get it.
            )
            
    def on_billing_update(mapper, connection, target):
        if target.payment_status == 'Pending':
            create_notification(
                notification_type='PAYMENT_PENDING',
                title='Pending Payment',
                message=f"Pending payment for invoice {target.invoice_number}. Total: ₹{target.total_amount}.",
                customer_id=None
            )

    event.listen(Billing, 'after_insert', on_billing_insert)
    event.listen(Billing, 'after_update', on_billing_update)

    # 4. APPOINTMENT REMINDER
    def on_appointment_insert(mapper, connection, target):
        if target.status == 'Pending':
            # Create a combined datetime for formatting
            dt = datetime.combine(target.appointment_date, target.appointment_time) if target.appointment_date and target.appointment_time else datetime.utcnow()
            create_notification(
                notification_type='APPOINTMENT_REMINDER',
                title='Appointment Reminder',
                message=f"Reminder: Your eye test appointment is scheduled on {dt.strftime('%Y-%m-%d %I:%M %p')}.",
                customer_id=target.customer_id
            )

    event.listen(Appointment, 'after_insert', on_appointment_insert)
