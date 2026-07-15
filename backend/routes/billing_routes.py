from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Invoice, InvoiceItem, Payment, Customer, Product
import uuid
from datetime import datetime

billing_bp = Blueprint('billing', __name__)

@billing_bp.route('/invoices', methods=['GET'])
@jwt_required()
def get_invoices():
    invoices = Invoice.query.order_by(Invoice.date.desc()).all()
    return jsonify([inv.to_dict() for inv in invoices]), 200

@billing_bp.route('/invoices/<int:id>', methods=['GET'])
@jwt_required()
def get_invoice(id):
    inv = Invoice.query.get_or_404(id)
    return jsonify(inv.to_dict()), 200

@billing_bp.route('/invoices', methods=['POST'])
@jwt_required()
def create_invoice():
    data = request.get_json()
    
    if 'customer_id' not in data or 'items' not in data:
        return jsonify({"message": "customer_id and items are required"}), 400
        
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
        
    items = data['items']
    if not items or len(items) == 0:
        return jsonify({"message": "Invoice must have at least one item"}), 400
        
    # Generate unique invoice number
    inv_number = f"INV-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    new_invoice = Invoice(
        invoice_number=inv_number,
        customer_id=customer.id,
        subtotal=float(data.get('subtotal', 0)),
        discount=float(data.get('discount', 0)),
        gst=float(data.get('gst', 0)),
        total=float(data.get('total', 0)),
        status=data.get('status', 'Pending')
    )
    
    db.session.add(new_invoice)
    db.session.flush() # Get invoice ID
    
    # Process items and deduct stock
    for item in items:
        # If product_id is provided, reduce stock
        if 'product_id' in item and item['product_id']:
            prod = Product.query.get(item['product_id'])
            if prod:
                qty = int(item.get('quantity', 1))
                if prod.stock >= qty:
                    prod.stock -= qty
                else:
                    db.session.rollback()
                    return jsonify({"message": f"Insufficient stock for {prod.name}"}), 400
        
        inv_item = InvoiceItem(
            invoice_id=new_invoice.id,
            product_id=item.get('product_id'),
            description=item.get('description'),
            quantity=int(item.get('quantity', 1)),
            price=float(item.get('price', 0))
        )
        db.session.add(inv_item)
        
    db.session.commit()
    
    return jsonify({"message": "Invoice created successfully", "invoice": new_invoice.to_dict()}), 201

@billing_bp.route('/payments', methods=['POST'])
@jwt_required()
def add_payment():
    data = request.get_json()
    
    required = ['invoice_id', 'amount', 'payment_mode']
    for req in required:
        if req not in data:
            return jsonify({"message": f"Missing {req}"}), 400
            
    invoice = Invoice.query.get_or_404(data['invoice_id'])
    
    payment = Payment(
        invoice_id=invoice.id,
        amount=float(data['amount']),
        payment_mode=data['payment_mode']
    )
    db.session.add(payment)
    
    # Update Invoice Status
    total_paid = sum([p.amount for p in invoice.payments]) + payment.amount
    if total_paid >= invoice.total:
        invoice.status = 'Paid'
    elif total_paid > 0:
        invoice.status = 'Partial'
        
    db.session.commit()
    
    return jsonify({"message": "Payment recorded successfully", "payment": payment.to_dict()}), 201
