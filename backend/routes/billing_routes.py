from flask import Blueprint, request, jsonify, send_file
from auth_utils import roles_required
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, decode_token
from models import db, Billing, Order, Customer, Payment, OrderStatusHistory, User
from datetime import datetime
import os
import uuid
from utils.pdf_generator import generate_invoice_pdf

billing_bp = Blueprint('billing', __name__)

def generate_invoice_number():
    date_str = datetime.utcnow().strftime('%Y')
    count = Billing.query.filter(Billing.invoice_number.like(f'VE-{date_str}-%')).count()
    return f'VE-{date_str}-{count + 1:04d}'

@billing_bp.route('/generate', methods=['POST'])
@roles_required('admin', 'staff')
def generate_bill():
    data = request.json or {}
    order_id = data.get('order_id')
    payment_method = data.get('payment_method', 'Cash')
    payment_status = data.get('payment_status', 'Paid')
    
    if not order_id:
        return jsonify({"message": "Order ID is required"}), 400
        
    order = Order.query.get_or_404(order_id)
    
    if order.billing:
        return jsonify({"message": "Order is already billed", "billing": order.billing.to_dict()}), 200
        
    if order.status == 'Cancelled':
        return jsonify({"message": "Cannot bill a cancelled order"}), 400
        
    customer = Customer.query.get(order.customer_id)
    
    subtotal = getattr(order, 'subtotal', None) or order.total_amount
    discount = getattr(order, 'discount', 0.0)
    gst = getattr(order, 'gst', 0.0)
    
    invoice_number = generate_invoice_number()
    billing = Billing(
        invoice_number=invoice_number,
        order_id=order.id,
        subtotal=subtotal,
        discount=discount,
        gst=gst,
        total_amount=order.total_amount,
        payment_method=payment_method,
        payment_status=payment_status
    )
    
    db.session.add(billing)
    db.session.flush() # get billing.id
    
    # Also record initial payment if Paid
    if payment_status == 'Paid':
        pmt = Payment(
            billing_id=billing.id,
            amount=order.total_amount,
            payment_method=payment_method,
            transaction_id=f"TXN-{uuid.uuid4().hex[:8].upper()}"
        )
        db.session.add(pmt)
    
    # Generate PDF
    try:
        order_items = [
            {
                "product_name": getattr(item, 'product_name', None) or f"Product #{item.product_id or item.id}",
                "item_type": getattr(item, 'product_type', None) or getattr(item, 'item_type', 'Frame'),
                "quantity": item.quantity,
                "unit_price": getattr(item, 'price', None) or getattr(item, 'unit_price', 0),
                "discount": getattr(item, 'discount', 0),
                "total_price": (item.quantity * getattr(item, 'price', 0)) if hasattr(item, 'price') else getattr(item, 'total_price', 0)
            } for item in order.items
        ]
        pdf_path = generate_invoice_pdf(billing, order_items, customer)
        billing.invoice_pdf = pdf_path
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Warning: PDF generation error: {e}")
        billing.invoice_pdf = None
        
    # Update Order Status
    order.status = 'Completed'
    
    history = OrderStatusHistory(
        order_id=order.id,
        status='Completed',
        notes=f'Invoice generated: {invoice_number}'
    )
    db.session.add(history)
    
    db.session.commit()
    
    return jsonify({
        "message": "Bill generated successfully",
        "billing": billing.to_dict()
    }), 201

@billing_bp.route('/', methods=['GET'])
@roles_required('admin', 'staff')
def get_bills():
    search = request.args.get('search')
    status = request.args.get('status')
    
    query = Billing.query
    
    if search:
        st = f"%{search}%"
        query = query.join(Order).join(Customer).filter(
            db.or_(
                Billing.invoice_number.ilike(st),
                Customer.first_name.ilike(st),
                Customer.last_name.ilike(st),
                Customer.phone.ilike(st)
            )
        )
        
    if status and status.lower() != 'all':
        query = query.filter(Billing.payment_status == status)
        
    bills = query.order_by(Billing.created_at.desc()).all()
    return jsonify([b.to_dict() for b in bills]), 200

@billing_bp.route('/stats', methods=['GET'])
@roles_required('admin', 'staff')
def get_stats():
    today = datetime.utcnow().date()
    
    total_bills = Billing.query.count()
    
    todays_bills = Billing.query.filter(db.func.date(Billing.created_at) == today).all()
    todays_sales = sum(b.total_amount for b in todays_bills if b.payment_status == 'Paid')
    
    current_month = datetime.utcnow().month
    monthly_bills = Billing.query.filter(db.func.extract('month', Billing.created_at) == current_month).all()
    monthly_revenue = sum(b.total_amount for b in monthly_bills if b.payment_status == 'Paid')
    
    pending_payments = Billing.query.filter(Billing.payment_status != 'Paid').count()
    
    return jsonify({
        "total_bills": total_bills,
        "todays_sales": todays_sales,
        "monthly_revenue": monthly_revenue,
        "pending_payments": pending_payments
    }), 200

@billing_bp.route('/payments', methods=['GET'])
@roles_required('admin', 'staff')
def get_all_payments():
    payments = Payment.query.order_by(Payment.payment_date.desc()).all()
    result = []
    for p in payments:
        b = p.billing
        customer_name = "Unknown"
        invoice_no = b.invoice_number if b else "N/A"
        if b and b.order_rel and b.order_rel.customer:
            c = b.order_rel.customer
            customer_name = f"{c.first_name} {c.last_name}"
        elif p.order_rel and p.order_rel.customer:
            c = p.order_rel.customer
            customer_name = f"{c.first_name} {c.last_name}"
            
        result.append({
            "id": p.id,
            "billing_id": p.billing_id,
            "order_id": p.order_id,
            "invoice_number": invoice_no,
            "customer_name": customer_name,
            "amount": float(p.amount) if p.amount is not None else 0.0,
            "payment_method": p.payment_method,
            "gateway": p.gateway or "Razorpay",
            "gateway_payment_id": p.gateway_payment_id,
            "gateway_order_id": p.gateway_order_id,
            "gateway_status": p.gateway_status or (b.payment_status if b else "Paid"),
            "refund_status": p.refund_status,
            "refunded_amount": float(p.refunded_amount or 0.0),
            "refund_id": p.refund_id,
            "transaction_id": p.gateway_payment_id or p.transaction_id,
            "payment_date": p.payment_date.isoformat() if p.payment_date else None,
            "status": b.payment_status if b else (p.gateway_status or "Paid")
        })
    return jsonify(result), 200

@billing_bp.route('/<int:id>', methods=['GET'])
@roles_required('admin', 'staff')
def get_bill(id):
    bill = Billing.query.get_or_404(id)
    return jsonify(bill.to_dict()), 200

@billing_bp.route('/<int:id>/payments', methods=['POST'])
@roles_required('admin', 'staff')
def record_payment(id):
    bill = Billing.query.get_or_404(id)
    data = request.get_json() or {}
    
    amount = float(data.get('amount', 0))
    payment_method = data.get('payment_method', 'Cash')
    transaction_id = data.get('transaction_id') or f"TXN-{uuid.uuid4().hex[:8].upper()}"
    
    if amount <= 0:
        return jsonify({"message": "Valid payment amount required"}), 400
        
    payment = Payment(
        billing_id=bill.id,
        amount=amount,
        payment_method=payment_method,
        transaction_id=transaction_id
    )
    db.session.add(payment)
    
    total_paid = sum(p.amount for p in bill.payments) + amount
    if total_paid >= bill.total_amount:
        bill.payment_status = 'Paid'
    else:
        bill.payment_status = 'Partial'
        
    db.session.commit()
    return jsonify({
        "message": "Payment recorded successfully",
        "payment": {
            "id": payment.id,
            "billing_id": payment.billing_id,
            "amount": payment.amount,
            "payment_method": payment.payment_method,
            "transaction_id": payment.transaction_id,
            "payment_date": str(payment.payment_date)
        },
        "invoice_status": bill.payment_status
    }), 201

@billing_bp.route('/<int:id>/pdf', methods=['GET'])
def download_invoice_pdf(id):
    """
    Download or generate the PDF invoice for a billing record.
    Supports Admin, Staff, and the Customer who owns the order.
    Accepts Authorization header OR ?token=<jwt> parameter for direct browser clicks.
    """
    token = request.args.get('token')
    user = None
    
    # 1. Try Authorization header
    try:
        verify_jwt_in_request(optional=True)
        uid = get_jwt_identity()
        if uid:
            user = User.query.get(int(uid))
    except Exception:
        pass
        
    # 2. Try query token parameter
    if not user and token:
        try:
            decoded = decode_token(token)
            uid = decoded.get('sub')
            if uid:
                user = User.query.get(int(uid))
        except Exception:
            pass

    if not user:
        return jsonify({"message": "Authentication required to download invoice"}), 401

    bill = Billing.query.get_or_404(id)
    
    # Permission verification
    role = (user.role or '').strip().lower()
    if role not in ('admin', 'staff'):
        order = bill.order_rel or Order.query.get(bill.order_id)
        if not order:
            return jsonify({"message": "Order not found"}), 404
            
        customer = order.customer
        allowed = False
        if customer:
            if getattr(customer, 'created_by', None) == user.id:
                allowed = True
            elif user.email and getattr(customer, 'email', None) and customer.email.lower() == user.email.lower():
                allowed = True
            elif user.phone and getattr(customer, 'phone', None) and customer.phone == user.phone:
                allowed = True
                
        if not allowed:
            return jsonify({"message": "You do not have permission to access this invoice."}), 403

    # Ensure PDF exists or generate on the fly
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, bill.invoice_pdf) if bill.invoice_pdf else None
    
    if not full_path or not os.path.exists(full_path):
        from utils.pdf_generator import generate_invoice_pdf
        rel_path = generate_invoice_pdf(bill)
        bill.invoice_pdf = rel_path
        db.session.commit()
        full_path = os.path.join(base_dir, rel_path)
        
    download_filename = f"VisionEdge_Invoice_{bill.invoice_number}.pdf"
    return send_file(
        full_path, 
        mimetype='application/pdf', 
        as_attachment=False, 
        download_name=download_filename
    )

@billing_bp.route('/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_bill(id):
    bill = Billing.query.get_or_404(id)
    try:
        if bill.invoice_pdf:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            pdf_path = os.path.join(base_dir, bill.invoice_pdf)
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
                
        order = Order.query.get(bill.order_id)
        if order:
            order.status = 'Ready'
            
        db.session.delete(bill)
        db.session.commit()
        return jsonify({"message": "Bill deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
