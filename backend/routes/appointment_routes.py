from flask import Blueprint, request, jsonify
from auth_utils import roles_required
from flask_jwt_extended import get_jwt_identity
from models import db, Appointment, Customer, User
from datetime import datetime, date, time
from sqlalchemy import or_

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/', methods=['GET'])
@roles_required('admin', 'staff')
def get_appointments():
    search = request.args.get('search')
    status = request.args.get('status')
    date_str = request.args.get('date')
    customer_id = request.args.get('customer_id')
    
    query = Appointment.query
    
    if status and status.lower() != 'all':
        query = query.filter(Appointment.status == status)
        
    if date_str:
        try:
            filter_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            query = query.filter(Appointment.appointment_date == filter_date)
        except ValueError:
            pass
            
    if customer_id:
        query = query.filter(Appointment.customer_id == customer_id)
        
    if search:
        st = f"%{search}%"
        query = query.join(Customer).filter(
            or_(
                Customer.first_name.ilike(st),
                Customer.last_name.ilike(st),
                Customer.phone.ilike(st),
                Appointment.doctor_name.ilike(st),
                Appointment.appointment_type.ilike(st)
            )
        )
        
    appointments = query.order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.desc()).all()
    return jsonify([a.to_dict() for a in appointments]), 200

@appointment_bp.route('/stats', methods=['GET'])
@roles_required('admin', 'staff')
def get_appointment_stats():
    today = datetime.utcnow().date()
    
    total = Appointment.query.count()
    today_count = Appointment.query.filter(Appointment.appointment_date == today).count()
    pending = Appointment.query.filter(Appointment.status == 'Pending').count()
    confirmed = Appointment.query.filter(Appointment.status == 'Confirmed').count()
    completed = Appointment.query.filter(Appointment.status == 'Completed').count()
    cancelled = Appointment.query.filter(Appointment.status == 'Cancelled').count()
    
    return jsonify({
        "total": total,
        "today": today_count,
        "pending": pending,
        "confirmed": confirmed,
        "completed": completed,
        "cancelled": cancelled
    }), 200

@appointment_bp.route('/<int:id>', methods=['GET'])
@roles_required('admin', 'staff')
def get_appointment(id):
    apt = Appointment.query.get_or_404(id)
    return jsonify(apt.to_dict()), 200

@appointment_bp.route('/', methods=['POST'])
def create_appointment():
    data = request.get_json() or {}
    
    customer_id = data.get('customer_id')
    
    # If no customer_id, check if customer details are provided to auto-lookup/create
    if not customer_id and (data.get('phone') or data.get('email')):
        phone = data.get('phone')
        cust = Customer.query.filter((Customer.phone == phone) | (Customer.email == data.get('email'))).first()
        if cust:
            customer_id = cust.id
        else:
            first_name = data.get('first_name') or 'Guest'
            last_name = data.get('last_name') or 'Customer'
            cust = Customer(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=data.get('email')
            )
            db.session.add(cust)
            db.session.commit()
            customer_id = cust.id
            
    if not customer_id:
        return jsonify({"message": "Customer ID or valid customer details required"}), 400
        
    apt_date_str = data.get('appointment_date') or data.get('date')
    apt_time_str = data.get('appointment_time') or data.get('time') or '10:00:00'
    
    if not apt_date_str:
        return jsonify({"message": "Appointment date required"}), 400
        
    try:
        if isinstance(apt_date_str, str) and 'T' in apt_date_str:
            apt_date_str = apt_date_str.split('T')[0]
        apt_date = datetime.strptime(str(apt_date_str), '%Y-%m-%d').date()
    except Exception:
        apt_date = datetime.utcnow().date()
        
    try:
        if len(apt_time_str) == 5:
            apt_time_str += ':00'
        apt_time = datetime.strptime(apt_time_str, '%H:%M:%S').time()
    except Exception:
        apt_time = time(10, 0, 0)
        
    apt = Appointment(
        customer_id=customer_id,
        appointment_date=apt_date,
        appointment_time=apt_time,
        appointment_type=data.get('appointment_type', 'Eye Test'),
        doctor_name=data.get('doctor_name', 'Dr. Sharma'),
        status=data.get('status', 'Pending'),
        notes=data.get('notes')
    )
    
    db.session.add(apt)
    db.session.commit()
    
    return jsonify({
        "message": "Appointment booked successfully",
        "appointment": apt.to_dict()
    }), 201

@appointment_bp.route('/<int:id>', methods=['PUT'])
@roles_required('admin', 'staff')
def update_appointment(id):
    apt = Appointment.query.get_or_404(id)
    data = request.get_json() or {}
    
    if 'status' in data:
        apt.status = data['status']
    if 'doctor_name' in data:
        apt.doctor_name = data['doctor_name']
    if 'appointment_type' in data:
        apt.appointment_type = data['appointment_type']
    if 'notes' in data:
        apt.notes = data['notes']
        
    if 'appointment_date' in data and data['appointment_date']:
        try:
            d_str = str(data['appointment_date']).split('T')[0]
            apt.appointment_date = datetime.strptime(d_str, '%Y-%m-%d').date()
        except Exception:
            pass
            
    if 'appointment_time' in data and data['appointment_time']:
        try:
            t_str = str(data['appointment_time'])
            if len(t_str) == 5:
                t_str += ':00'
            apt.appointment_time = datetime.strptime(t_str, '%H:%M:%S').time()
        except Exception:
            pass
            
    db.session.commit()
    return jsonify({
        "message": "Appointment updated successfully",
        "appointment": apt.to_dict()
    }), 200

@appointment_bp.route('/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_appointment(id):
    apt = Appointment.query.get_or_404(id)
    db.session.delete(apt)
    db.session.commit()
    return jsonify({"message": "Appointment deleted successfully"}), 200
