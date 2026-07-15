from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Customer
from datetime import datetime

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/', methods=['GET'])
@jwt_required()
def get_customers():
    customers = Customer.query.order_by(Customer.created_at.desc()).all()
    return jsonify([customer.to_dict() for customer in customers]), 200

@customer_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify(customer.to_dict()), 200

@customer_bp.route('/', methods=['POST'])
@jwt_required()
def create_customer():
    data = request.get_json()
    
    required_fields = ['first_name', 'last_name', 'phone']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing required field: {field}"}), 400
            
    dob = None
    if data.get('dob'):
        try:
            dob = datetime.strptime(data.get('dob'), '%Y-%m-%d').date()
        except ValueError:
            pass
            
    new_customer = Customer(
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        email=data.get('email'),
        gender=data.get('gender'),
        dob=dob,
        address=data.get('address')
    )
    
    db.session.add(new_customer)
    db.session.commit()
    
    return jsonify({"message": "Customer created successfully", "customer": new_customer.to_dict()}), 201

@customer_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json()
    
    if 'first_name' in data: customer.first_name = data['first_name']
    if 'last_name' in data: customer.last_name = data['last_name']
    if 'phone' in data: customer.phone = data['phone']
    if 'email' in data: customer.email = data['email']
    if 'gender' in data: customer.gender = data['gender']
    if 'address' in data: customer.address = data['address']
    
    if 'dob' in data:
        try:
            customer.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date() if data['dob'] else None
        except ValueError:
            pass
            
    db.session.commit()
    return jsonify({"message": "Customer updated successfully", "customer": customer.to_dict()}), 200

@customer_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully"}), 200
