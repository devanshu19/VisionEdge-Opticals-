from app import create_app, db
from models import Customer, Order, Billing, Appointment, Prescription, EyeTest, OrderItem, OrderStatusHistory, CustomerProfile, Notification, Payment
from sqlalchemy import text

app = create_app()
with app.app_context():
    dummy_cust_ids = [c.id for c in Customer.query.filter(Customer.first_name.like('Test%')).all()]
    dummy_orders = Order.query.filter(Order.order_number.like('ORD0%')).all()
    dummy_order_ids = [o.id for o in dummy_orders]
    dummy_billings = Billing.query.filter(Billing.invoice_number.like('INV0%')).all()
    dummy_billing_ids = [b.id for b in dummy_billings]

    print(f"Purging {len(dummy_order_ids)} dummy orders, {len(dummy_billing_ids)} dummy billings, {len(dummy_cust_ids)} dummy customers...")

    # 1. Delete payments on dummy billings
    if dummy_billing_ids:
        Payment.query.filter(Payment.billing_id.in_(dummy_billing_ids)).delete(synchronize_session=False)

    # 2. Delete dummy billings
    if dummy_billing_ids:
        Billing.query.filter(Billing.id.in_(dummy_billing_ids)).delete(synchronize_session=False)

    # 3. Delete dummy order items & status history & orders
    if dummy_order_ids:
        OrderItem.query.filter(OrderItem.order_id.in_(dummy_order_ids)).delete(synchronize_session=False)
        OrderStatusHistory.query.filter(OrderStatusHistory.order_id.in_(dummy_order_ids)).delete(synchronize_session=False)
        Order.query.filter(Order.id.in_(dummy_order_ids)).delete(synchronize_session=False)

    # 4. Delete dummy appointments
    if dummy_cust_ids:
        Appointment.query.filter(Appointment.customer_id.in_(dummy_cust_ids)).delete(synchronize_session=False)

    # 5. Delete dummy prescriptions & eye tests
    if dummy_cust_ids:
        Prescription.query.filter(Prescription.customer_id.in_(dummy_cust_ids)).delete(synchronize_session=False)
        EyeTest.query.filter(EyeTest.customer_id.in_(dummy_cust_ids)).delete(synchronize_session=False)

    # 6. Delete dummy customer profiles & customers
    if dummy_cust_ids:
        CustomerProfile.query.filter(CustomerProfile.customer_id.in_(dummy_cust_ids)).delete(synchronize_session=False)
        Customer.query.filter(Customer.id.in_(dummy_cust_ids)).delete(synchronize_session=False)

    # 7. Clean dummy notifications
    Notification.query.filter(Notification.message.like('%Test%')).delete(synchronize_session=False)
    Notification.query.filter(Notification.message.like('%ORD0%')).delete(synchronize_session=False)

    # 8. Clean dummy inventory transactions
    db.session.execute(text("DELETE FROM inventory_transaction WHERE notes LIKE '%ORD0%' OR notes LIKE '%Test%'"))

    db.session.commit()
    print("ALL DUMMY DATABASE RECORDS PURGED SUCCESSFULLY!")
