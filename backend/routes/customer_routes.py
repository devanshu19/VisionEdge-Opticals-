from flask import Blueprint, request, jsonify
from auth_utils import roles_required
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import db, Customer, User, Order, Prescription, Appointment, Billing
from datetime import datetime
from sqlalchemy import or_

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/stats', methods=['GET'])
@roles_required('admin', 'staff')
def get_stats():
    total = Customer.query.count()
    active = Customer.query.filter_by(status='Active').count()
    inactive = Customer.query.filter_by(status='Inactive').count()
    
    today = datetime.utcnow().date()
    # Simple count of customers created today
    today_new = Customer.query.filter(Customer.created_at >= str(today)).count()
    
    return jsonify({
        "total": total,
        "active": active,
        "inactive": inactive,
        "today_new": today_new
    }), 200

@customer_bp.route('/', methods=['GET'])
@roles_required('admin', 'staff')
def get_customers():
    query = Customer.query
    
    search = request.args.get('search', '')
    status = request.args.get('status', 'all')
    
    if status.lower() != 'all':
        query = query.filter(Customer.status == status.capitalize())
        
    if search:
        search_term = f"%{search}%"
        query = query.filter(or_(
            Customer.customer_code.ilike(search_term),
            Customer.first_name.ilike(search_term),
            Customer.last_name.ilike(search_term),
            Customer.phone.ilike(search_term),
            Customer.email.ilike(search_term),
            Customer.city.ilike(search_term)
        ))
        
    customers = query.order_by(Customer.created_at.desc()).all()
    return jsonify([customer.to_dict() for customer in customers]), 200

@customer_bp.route('/<int:id>', methods=['GET'])
@roles_required('admin', 'staff')
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify(customer.to_dict()), 200

@customer_bp.route('/', methods=['POST'])
@roles_required('admin', 'staff')
def create_customer():
    data = request.get_json()
    
    required_fields = ['first_name', 'last_name', 'phone', 'gender']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"Missing required field: {field}"}), 400
            
    # Phone must be unique
    if Customer.query.filter_by(phone=data['phone']).first():
        return jsonify({"message": "Phone number is already registered"}), 400
        
    dob = None
    if data.get('dob'):
        try:
            dob = datetime.strptime(data.get('dob'), '%Y-%m-%d').date()
        except ValueError:
            pass
            
    # Auto-generate customer_code (e.g., CUST0001)
    last_customer = Customer.query.order_by(Customer.id.desc()).first()
    next_id = last_customer.id + 1 if last_customer else 1
    customer_code = f"CUST{next_id:04d}"
            
    new_customer = Customer(
        customer_code=customer_code,
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        alternate_phone=data.get('alternate_phone'),
        email=data.get('email'),
        gender=data.get('gender'),
        date_of_birth=dob,
        occupation=data.get('occupation'),
        address=data.get('address'),
        city=data.get('city'),
        state=data.get('state'),
        pincode=data.get('pincode'),
        status=data.get('status', 'Active'),
        created_by=int(get_jwt_identity()) if get_jwt_identity() else None
    )
    
    db.session.add(new_customer)
    db.session.flush() # To get the new_customer.id
    
    from models import CustomerProfile
    profile = CustomerProfile(
        customer_id=new_customer.id,
        blood_group=data.get('blood_group'),
        eye_conditions=data.get('eye_condition'),
        allergies=data.get('allergies'),
        notes=data.get('notes')
    )
    db.session.add(profile)
    db.session.commit()
    
    return jsonify({"message": "Customer created successfully", "customer": new_customer.to_dict()}), 201

@customer_bp.route('/<int:id>', methods=['PUT'])
@roles_required('admin', 'staff')
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json()
    
    if 'phone' in data and data['phone'] != customer.phone:
        if Customer.query.filter_by(phone=data['phone']).first():
            return jsonify({"message": "Phone number is already registered to another customer"}), 400
    
    fields = [
        'first_name', 'last_name', 'phone', 'alternate_phone', 'email', 'gender',
        'occupation', 'address', 'city', 'state', 'pincode', 'status'
    ]
    
    for field in fields:
        if field in data:
            setattr(customer, field, data[field])
    
    if 'dob' in data:
        try:
            customer.date_of_birth = datetime.strptime(data['dob'], '%Y-%m-%d').date() if data['dob'] else None
        except ValueError:
            pass
            
    customer.updated_at = datetime.utcnow()
    
    if customer.profile:
        if 'blood_group' in data: customer.profile.blood_group = data['blood_group']
        if 'eye_condition' in data: customer.profile.eye_conditions = data['eye_condition']
        if 'allergies' in data: customer.profile.allergies = data['allergies']
        if 'notes' in data: customer.profile.notes = data['notes']
    
    db.session.commit()
    
    return jsonify({"message": "Customer updated successfully", "customer": customer.to_dict()}), 200

@customer_bp.route('/<int:id>', methods=['DELETE'])
@customer_bp.route('/<int:id>/', methods=['DELETE'])
@roles_required('admin')
def delete_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({"message": "Customer not found."}), 404
        
    try:
        from models import Order, OrderItem, Billing, Payment, EyeTest, Prescription, VirtualTryOnHistory, FrameRecommendation, Appointment
        
        # 1. Delete associated appointments
        Appointment.query.filter_by(customer_id=id).delete(synchronize_session=False)

        # 2. Delete associated orders, order items, billing, and payments
        orders = Order.query.filter_by(customer_id=id).all()
        for ord_obj in orders:
            OrderItem.query.filter_by(order_id=ord_obj.id).delete(synchronize_session=False)
            billings = Billing.query.filter_by(order_id=ord_obj.id).all()
            for bill in billings:
                Payment.query.filter_by(billing_id=bill.id).delete(synchronize_session=False)
                db.session.delete(bill)
            db.session.delete(ord_obj)
            
        # 3. Delete eye tests and prescriptions
        EyeTest.query.filter_by(customer_id=id).delete(synchronize_session=False)
        Prescription.query.filter_by(customer_id=id).delete(synchronize_session=False)
        
        # 4. Delete AI & VTO records
        VirtualTryOnHistory.query.filter_by(customer_id=id).delete(synchronize_session=False)
        FrameRecommendation.query.filter_by(customer_id=id).delete(synchronize_session=False)
        
        # 5. Delete customer profile if exists
        if hasattr(customer, 'profile') and customer.profile:
            db.session.delete(customer.profile)
            
        # 6. Delete customer record
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": "Customer deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Cannot delete customer: {str(e)}"}), 400

# ==================================================
# CUSTOMER DASHBOARD (LIVE SUMMARY)
# ==================================================
@customer_bp.route('/my-dashboard', methods=['GET'])
@jwt_required()
def my_dashboard():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        customer = Customer.query.filter_by(created_by=user.id).first()
        if not customer and user.phone:
            customer = Customer.query.filter_by(phone=user.phone).first()
        if not customer and user.email:
            customer = Customer.query.filter_by(email=user.email).first()

        if not customer:
            return jsonify({
                "active_orders": 0,
                "prescriptions_count": 0,
                "reward_points": 0,
                "upcoming_appointment": None,
                "recent_orders": []
            }), 200

        # Orders
        all_orders = Order.query.filter_by(customer_id=customer.id).order_by(Order.created_at.desc()).all()
        active_statuses = ['Pending', 'Confirmed', 'Processing', 'Ready', 'Ready for Pickup']
        active_orders_count = sum(1 for o in all_orders if o.status in active_statuses)

        recent_orders_list = []
        for o in all_orders[:5]:
            b = getattr(o, 'billing', None)
            items_desc = []
            if hasattr(o, 'items'):
                for it in o.items:
                    name = ""
                    if hasattr(it, 'frame') and it.frame:
                        name = f"{it.frame.brand} {it.frame.model}"
                    elif hasattr(it, 'lens') and it.lens:
                        name = f"{it.lens.type} Lens"
                    if name:
                        items_desc.append(name)
            
            desc = ", ".join(items_desc) if items_desc else "Optical Eyewear"
            recent_orders_list.append({
                "id": o.id,
                "order_number": o.order_number or o.order_id or f"ORD-{o.id}",
                "created_at": str(o.created_at),
                "date": o.created_at.strftime('%b %d, %Y') if o.created_at else "—",
                "items_desc": desc,
                "status": o.status,
                "total_amount": float(o.total_amount or 0),
                "payment_status": b.payment_status if b else 'Pending'
            })

        # Prescriptions
        prescriptions_count = Prescription.query.filter_by(customer_id=customer.id).count()

        # Reward points: 5% of completed purchases
        completed_spend = sum(float(o.total_amount or 0) for o in all_orders if o.status in ['Delivered', 'Completed'])
        reward_points = int(completed_spend * 0.05)

        # Appointments
        today = datetime.utcnow().date()
        upcoming_appt = (Appointment.query
                         .filter(Appointment.customer_id == customer.id,
                                 Appointment.appointment_date >= today,
                                 Appointment.status.in_(['Pending', 'Confirmed']))
                         .order_by(Appointment.appointment_date.asc(), Appointment.appointment_time.asc())
                         .first())

        appt_data = None
        if upcoming_appt:
            appt_data = {
                "id": upcoming_appt.id,
                "date": str(upcoming_appt.appointment_date),
                "month": upcoming_appt.appointment_date.strftime('%b').upper(),
                "day": upcoming_appt.appointment_date.strftime('%d'),
                "time": str(upcoming_appt.appointment_time)[:5] if upcoming_appt.appointment_time else "10:00",
                "type": upcoming_appt.appointment_type or "Comprehensive Exam",
                "status": upcoming_appt.status,
                "doctor": upcoming_appt.doctor_name or "Store Optometrist",
                "location": "Opp. Sardar Patel Stadium, Navrangpura, Ahmedabad"
            }

        return jsonify({
            "active_orders": active_orders_count,
            "prescriptions_count": prescriptions_count,
            "reward_points": reward_points,
            "upcoming_appointment": appt_data,
            "recent_orders": recent_orders_list
        }), 200
    except Exception as e:
        return jsonify({"message": "Failed to load dashboard data", "error": str(e)}), 500

