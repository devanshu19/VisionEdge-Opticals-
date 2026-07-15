from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Prescription, Customer
from datetime import datetime

prescription_bp = Blueprint('prescription', __name__)

@prescription_bp.route('/', methods=['GET'])
@jwt_required()
def get_prescriptions():
    customer_id = request.args.get('customer_id')
    query = Prescription.query
    
    if customer_id:
        query = query.filter_by(customer_id=customer_id)
        
    prescriptions = query.order_by(Prescription.date.desc()).all()
    return jsonify([rx.to_dict() for rx in prescriptions]), 200

@prescription_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_prescription(id):
    rx = Prescription.query.get_or_404(id)
    return jsonify(rx.to_dict()), 200

@prescription_bp.route('/', methods=['POST'])
@jwt_required()
def create_prescription():
    data = request.get_json()
    
    if 'customer_id' not in data:
        return jsonify({"message": "customer_id is required"}), 400
        
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
        
    try:
        rx_date = datetime.strptime(data.get('date', datetime.utcnow().strftime('%Y-%m-%d')), '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"message": "Invalid date format, use YYYY-MM-DD"}), 400

    expiry_date = None
    if data.get('expiry_date'):
        try:
            expiry_date = datetime.strptime(data['expiry_date'], '%Y-%m-%d').date()
        except ValueError:
            pass

    od = data.get('od', {})
    os = data.get('os', {})
    
    new_rx = Prescription(
        customer_id=customer.id,
        date=rx_date,
        expiry_date=expiry_date,
        od_sph=od.get('sph'), od_cyl=od.get('cyl'), od_axis=od.get('axis'), od_add=od.get('add'), od_pd=od.get('pd'),
        os_sph=os.get('sph'), os_cyl=os.get('cyl'), os_axis=os.get('axis'), os_add=os.get('add'), os_pd=os.get('pd'),
        notes=data.get('notes')
    )
    
    db.session.add(new_rx)
    db.session.commit()
    
    return jsonify({"message": "Prescription created successfully", "prescription": new_rx.to_dict()}), 201
