from models import db, Notification

def create_notification(notification_type, title, message, user_id=None, customer_id=None):
    """
    Creates a notification in the database.
    If user_id is None, it acts as a system broadcast to admins.
    """
    try:
        from datetime import datetime
        db.session.execute(
            db.text("INSERT INTO notification (user_id, customer_id, notification_type, title, message, status, created_at) VALUES (:u, :c, :nt, :t, :m, 'Unread', :dt)"),
            {"u": user_id, "c": customer_id, "nt": notification_type, "t": title, "m": message, "dt": datetime.utcnow()}
        )
        
        class MockNotif:
            pass
        n = MockNotif()
        n.customer_id = customer_id
        n.notification_type = notification_type
        n.title = title
        n.message = message
        
        # Trigger external APIs in the future
        _trigger_external_apis(n)
        
        return True
    except Exception as e:
        print("Error creating notification:", e)
        return False

def _trigger_external_apis(notification):
    """
    Routes notifications to external APIs (Email) based on preference or type.
    """
    if notification.customer_id:
        if notification.notification_type in ['ORDER_READY', 'ORDER_COMPLETED', 'APPOINTMENT_REMINDER']:
            send_email_notification(notification.customer_id, notification.title, notification.message)

def send_email_notification(customer_id, subject, body):
    """
    Email notification dispatcher
    """
    print(f"[EMAIL NOTIFICATION] To Customer {customer_id}: [{subject}] {body}")
    pass
