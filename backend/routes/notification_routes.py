from flask import Blueprint, request, jsonify
from auth_utils import roles_required
from flask_jwt_extended import get_jwt_identity
from models import db, Notification, User

notification_bp = Blueprint('notifications', __name__)

@notification_bp.route('/', methods=['GET'])
@roles_required('admin', 'staff')
def get_notifications():
    # If user is admin/staff, they see system notifications (customer_id is null) 
    # and maybe they can see all. The prompt says Admin receives Inventory, Sales, Orders.
    # We will just fetch notifications where customer_id is None for staff dashboard.
    notifications = Notification.query.filter_by(customer_id=None).order_by(Notification.created_at.desc()).limit(50).all()
    return jsonify([n.to_dict() for n in notifications]), 200

@notification_bp.route('/customer/<int:customer_id>', methods=['GET'])
@roles_required('admin', 'staff')
def get_customer_notifications(customer_id):
    notifications = Notification.query.filter_by(customer_id=customer_id).order_by(Notification.created_at.desc()).limit(20).all()
    return jsonify([n.to_dict() for n in notifications]), 200

@notification_bp.route('/count', methods=['GET'])
@roles_required('admin', 'staff')
def get_unread_count():
    count = Notification.query.filter_by(customer_id=None, status='Unread').count()
    return jsonify({"unread": count}), 200

@notification_bp.route('/read/<int:notif_id>', methods=['POST'])
@roles_required('admin', 'staff')
def mark_as_read(notif_id):
    notif = Notification.query.get(notif_id)
    if notif:
        notif.status = 'Read'
        db.session.commit()
        return jsonify({"message": "Marked as read"}), 200
    return jsonify({"message": "Not found"}), 404

@notification_bp.route('/read-all', methods=['POST'])
@roles_required('admin', 'staff')
def mark_all_as_read():
    db.session.query(Notification).filter_by(customer_id=None, status='Unread').update({"status": "Read"})
    db.session.commit()
    return jsonify({"message": "All marked as read"}), 200
