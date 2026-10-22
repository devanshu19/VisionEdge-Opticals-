from flask import Blueprint, request, jsonify, send_file
from auth_utils import roles_required
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request, decode_token
from models import db, Order, OrderItem, OrderStatusHistory, InventoryTransaction, Frame, Lens, Customer, Prescription, User, Billing, Payment
from datetime import datetime
import uuid
import os

order_bp = Blueprint('order', __name__)

def generate_order_number():
    date_str = datetime.utcnow().strftime('%Y%m')
    count = Order.query.filter(Order.order_number.like(f'ORD-{date_str}-%')).count()
    return f'ORD-{date_str}-{count + 1:03d}'

@order_bp.route('/', methods=['POST'])
@roles_required('admin', 'staff')
def create_order():
    current_user_id = get_jwt_identity()
    data = request.json
    try:
        if not data.get('customer_id') or not data.get('items'):
            return jsonify({"message": "Customer ID and Items are required"}), 400
            
        customer = Customer.query.get(data['customer_id'])
        if not customer:
            return jsonify({"message": "Customer not found"}), 404
            
        order = Order(
            order_number=generate_order_number(),
            customer_id=data['customer_id'],
            prescription_id=data.get('prescription_id'),
            expected_delivery_date=datetime.strptime(data['expected_delivery_date'], '%Y-%m-%d') if data.get('expected_delivery_date') else None,
            sales_person_id=current_user_id,
            priority=data.get('priority', 'Normal'),
            status='Pending',
            notes=data.get('notes')
        )
        db.session.add(order)
        db.session.flush() # Get order.id
        
        subtotal = 0.0
        gst_total = 0.0
        discount_total = float(data.get('discount', 0))
        
        for item_data in data['items']:
            item_type = item_data['item_type'] # 'Frame' or 'Lens'
            item_id = item_data['item_id']
            qty = int(item_data['quantity'])
            
            if item_type == 'Frame':
                product = Frame.query.get(item_id)
            elif item_type == 'Lens':
                product = Lens.query.get(item_id)
            else:
                return jsonify({"message": f"Invalid item type: {item_type}"}), 400
                
            if not product:
                return jsonify({"message": f"{item_type} not found"}), 404
                
            if product.stock < qty:
                return jsonify({"message": f"Insufficient stock for {product.name}"}), 400
                
            # Stock deduction and InventoryTransaction are now handled automatically 
            # by SQLAlchemy after_insert hooks in utils/signals.py
            
            # Calculate item pricing
            price_val = product.selling_price if (hasattr(product, 'selling_price') and product.selling_price is not None) else product.price
            unit_price = float(price_val) if price_val is not None else 0.0
            item_discount = float(item_data.get('discount', 0))
            item_subtotal = (unit_price * qty) - item_discount
            gst_perc = getattr(product, 'gst_percent', 0.0) or 0.0
            item_gst = item_subtotal * (gst_perc / 100.0) if gst_perc else 0.0
            item_total = item_subtotal + item_gst
            
            subtotal += item_subtotal
            gst_total += item_gst
            
            order_item = OrderItem(
                order_id=order.id,
                item_type=item_type,
                item_id=item_id,
                quantity=qty,
                unit_price=unit_price,
                discount=item_discount,
                gst=item_gst,
                total_price=item_total
            )
            db.session.add(order_item)
            
        order.subtotal = subtotal
        order.gst = gst_total
        order.discount = discount_total
        order.total_amount = subtotal + gst_total - discount_total
        
        # Initial status history
        history = OrderStatusHistory(
            order_id=order.id,
            status='Pending',
            remarks='Order created',
            user_id=current_user_id
        )
        db.session.add(history)
        
        db.session.commit()
        return jsonify({"message": "Order created successfully", "order_id": order.id, "order_number": order.order_number}), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating order: {str(e)}")
        return jsonify({"message": "Failed to create order"}), 500

@order_bp.route('/', methods=['GET'])
@roles_required('admin', 'staff')
def get_orders():
    status = request.args.get('status')
    customer_id = request.args.get('customer_id')
    search = request.args.get('search')
    
    query = Order.query
    
    if status:
        query = query.filter_by(status=status)
    if customer_id:
        query = query.filter_by(customer_id=customer_id)
    if search:
        query = query.join(Customer).filter(
            db.or_(
                Order.order_number.ilike(f'%{search}%'),
                Customer.first_name.ilike(f'%{search}%'),
                Customer.last_name.ilike(f'%{search}%'),
                Customer.phone.ilike(f'%{search}%')
            )
        )
        
    orders = query.order_by(Order.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders])

@order_bp.route('/<int:id>', methods=['GET'])
@roles_required('admin', 'staff')
def get_order(id):
    order = Order.query.get_or_404(id)
    order_dict = order.to_dict()
    
    # Hydrate items with product details
    for item in order_dict['items']:
        if item['item_type'] == 'Frame':
            p = Frame.query.get(item['item_id'])
            item['product_name'] = p.name if p else 'Unknown Frame'
            item['product_code'] = p.frame_code if p else 'N/A'
        elif item['item_type'] == 'Lens':
            p = Lens.query.get(item['item_id'])
            item['product_name'] = p.name if p else 'Unknown Lens'
            item['product_code'] = p.lens_code if p else 'N/A'
            
    # Add Prescription details if any
    if order.prescription:
        order_dict['prescription_details'] = order.prescription.to_dict()
        
    # Add Customer details
    order_dict['customer_details'] = order.customer.to_dict()
            
    return jsonify(order_dict)

@order_bp.route('/<int:id>/status', methods=['PUT'])
@roles_required('admin', 'staff')
def update_status(id):
    current_user_id = get_jwt_identity()
    order = Order.query.get_or_404(id)
    data = request.json
    new_status = data.get('status')
    remarks = data.get('remarks', '')
    
    if not new_status:
        return jsonify({"message": "Status is required"}), 400
        
    if order.status == new_status:
        return jsonify({"message": "Order is already in this status"}), 400
        
    try:
        # If order is being cancelled, restore inventory
        if new_status == 'Cancelled' and order.status != 'Cancelled':
            for item in order.items:
                if item.item_type == 'Frame':
                    product = Frame.query.get(item.item_id)
                else:
                    product = Lens.query.get(item.item_id)
                    
                if product:
                    product.stock += item.quantity
                    tx = InventoryTransaction(
                        item_type=item.item_type,
                        item_id=item.item_id,
                        transaction_type='Return',
                        quantity=item.quantity,
                        reason=f'Order {order.order_number} Cancelled',
                        reference_number=order.order_number,
                        user_id=current_user_id
                    )
                    db.session.add(tx)
                    
        # If it was cancelled but now un-cancelled (e.g. restored to Pending) - we need to reserve stock again
        if order.status == 'Cancelled' and new_status != 'Cancelled':
            for item in order.items:
                if item.item_type == 'Frame':
                    product = Frame.query.get(item.item_id)
                else:
                    product = Lens.query.get(item.item_id)
                    
                if product:
                    if product.stock < item.quantity:
                        return jsonify({"message": f"Cannot un-cancel: Insufficient stock for {product.name}"}), 400
                    product.stock -= item.quantity
                    tx = InventoryTransaction(
                        item_type=item.item_type,
                        item_id=item.item_id,
                        transaction_type='Sale',
                        quantity=item.quantity,
                        reason=f'Order {order.order_number} Restored',
                        reference_number=order.order_number,
                        user_id=current_user_id
                    )
                    db.session.add(tx)
                    
        if new_status == 'Delivered':
            order.actual_delivery_date = datetime.utcnow().date()
            
        order.status = new_status
        history = OrderStatusHistory(
            order_id=order.id,
            status=new_status,
            remarks=remarks,
            user_id=current_user_id
        )
        db.session.add(history)
        db.session.commit()
        
        return jsonify({"message": "Status updated successfully"})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to update status"}), 500

@order_bp.route('/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_order(id):
    order = Order.query.get_or_404(id)
    try:
        # Restore stock if it hasn't been cancelled yet
        if order.status != 'Cancelled':
            for item in order.items:
                if item.item_type == 'Frame':
                    product = Frame.query.get(item.item_id)
                else:
                    product = Lens.query.get(item.item_id)
                if product:
                    product.stock += item.quantity
                    
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to delete order"}), 500

@order_bp.route('/stats', methods=['GET'])
@roles_required('admin', 'staff')
def get_stats():
    today = datetime.utcnow().date()
    
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status='Pending').count()
    ready_orders = Order.query.filter_by(status='Ready for Pickup').count()
    todays_orders = Order.query.filter(db.func.date(Order.created_at) == today).count()
    
    return jsonify({
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "ready_orders": ready_orders,
        "todays_orders": todays_orders
    })

@order_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    try:
        if not data.get('items'):
            return jsonify({"message": "Items are required"}), 400

        # Find or create Customer record for this user
        customer = Customer.query.filter_by(created_by=user.id).first()
        if not customer:
            # Fallback to match by phone or email
            customer = Customer.query.filter_by(phone=user.phone).first() if user.phone else None
            if not customer and user.email:
                customer = Customer.query.filter_by(email=user.email).first()
            
            if not customer:
                # Create a new Customer profile
                last_customer = Customer.query.order_by(Customer.id.desc()).first()
                next_id = last_customer.id + 1 if last_customer else 1
                customer_code = f"CUST{next_id:04d}"
                
                customer = Customer(
                    customer_code=customer_code,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    phone=user.phone or data.get('phone', '0000000000'),
                    email=user.email,
                    address=data.get('shipping_address', user.address),
                    created_by=user.id
                )
                db.session.add(customer)
                db.session.flush()

        ord_num = generate_order_number()
        order = Order(
            order_id=ord_num,
            order_number=ord_num,
            customer_id=customer.id,
            status='Pending'
        )
        db.session.add(order)
        db.session.flush()

        subtotal = 0.0
        gst_total = 0.0
        
        for item_data in data['items']:
            item_type = item_data.get('item_type', 'Frame')
            item_id = item_data['item_id']
            qty = int(item_data['quantity'])
            
            if item_type == 'Frame':
                product = Frame.query.get(item_id)
            else:
                product = Lens.query.get(item_id)
                
            if not product:
                return jsonify({"message": f"{item_type} not found"}), 404
                
            if product.stock < qty:
                return jsonify({"message": f"Insufficient stock for {product.name}"}), 400
                
            price_val = product.selling_price if (hasattr(product, 'selling_price') and product.selling_price is not None) else product.price
            unit_price = float(price_val) if price_val is not None else 0.0
            item_subtotal = unit_price * qty
            gst_perc = getattr(product, 'gst_percent', 0.0) or 0.0
            item_gst = item_subtotal * (gst_perc / 100.0) if gst_perc else 0.0
            item_total = item_subtotal + item_gst
            
            subtotal += item_subtotal
            gst_total += item_gst
            
            order_item = OrderItem(
                order_id=order.id,
                item_type=item_type,
                item_id=item_id,
                quantity=qty,
                unit_price=unit_price,
                total_price=item_total
            )
            db.session.add(order_item)
            
        discount_val = float(data.get('discount', 0.0) or 0.0)
        order.subtotal = subtotal
        order.gst = gst_total
        order.discount = discount_val
        order.total_amount = max(0.0, subtotal + gst_total - discount_val)
        
        payment_method = data.get('payment_method', 'Cash on Delivery')
        is_cod = str(payment_method).strip().lower() in ('cash on delivery', 'cod')

        if not is_cod:
            # Online orders MUST go through verified gateway flow (/api/payment/razorpay/create-order)
            return jsonify({
                "message": "Online payments must be processed securely through the Razorpay gateway.",
                "redirect_to": "/api/payment/razorpay/create-order"
            }), 400

        # Cash on Delivery flow
        payment_status = 'Pending'
        order.status = 'Pending'
        txn_id = f"VE-COD-{uuid.uuid4().hex[:8].upper()}"

        # Initial status history
        history = OrderStatusHistory(
            order_id=order.id,
            status=order.status,
            notes=f"Order placed online via Cash on Delivery. TxnID: {txn_id}" + (f" (Coupon Discount: ₹{discount_val:.2f})" if discount_val > 0 else "")
        )
        db.session.add(history)
        
        # Automatically generate invoice/billing
        from routes.billing_routes import generate_invoice_number
        invoice_number = generate_invoice_number()
        billing = Billing(
            invoice_number=invoice_number,
            order_id=order.id,
            subtotal=subtotal,
            discount=discount_val,
            gst=gst_total,
            total_amount=order.total_amount,
            payment_method='Cash on Delivery',
            payment_status='Pending'
        )
        db.session.add(billing)
        db.session.flush()

        payment = Payment(
            billing_id=billing.id,
            order_id=order.id,
            amount=order.total_amount,
            currency='INR',
            transaction_id=txn_id,
            payment_method='Cash on Delivery',
            gateway='COD',
            gateway_status='pending',
            signature_verified=False
        )
        db.session.add(payment)
        
        db.session.commit()
        return jsonify({
            "message": "Order placed successfully",
            "order_id": order.id,
            "order_number": order.order_number,
            "invoice_number": invoice_number,
            "total_amount": float(order.total_amount),
            "transaction_id": txn_id,
            "payment_status": payment_status,
            "payment_method": payment_method
        }), 201
        
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({"message": "Failed to process checkout"}), 500

@order_bp.route('/<int:id>/invoice-pdf', methods=['GET'])
def download_order_invoice_pdf(id):
    """
    Allows downloading or streaming the PDF invoice directly by Order ID.
    Auto-creates the Billing record and PDF invoice if not yet present.
    """
    token = request.args.get('token')
    user = None
    
    try:
        verify_jwt_in_request(optional=True)
        uid = get_jwt_identity()
        if uid:
            user = User.query.get(int(uid))
    except Exception:
        pass
        
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

    order = Order.query.get_or_404(id)
    
    role = (user.role or '').strip().lower()
    if role not in ('admin', 'staff'):
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
            return jsonify({"message": "You do not have permission to access this order's invoice."}), 403

    bill = order.billing or Billing.query.filter_by(order_id=order.id).first()
    if not bill:
        from routes.billing_routes import generate_invoice_number
        subtotal = float(order.subtotal or order.total_amount or 0.0)
        discount = float(order.discount or 0.0)
        gst_val = float(order.gst or 0.0)
        total = float(order.total_amount or (subtotal - discount + gst_val))
        bill = Billing(
            invoice_number=generate_invoice_number(),
            order_id=order.id,
            subtotal=subtotal,
            discount=discount,
            gst=gst_val,
            total_amount=total,
            payment_status='Paid' if order.status in ('Confirmed', 'Processing', 'Delivered', 'Completed') else 'Pending',
            payment_method='Razorpay Online'
        )
        db.session.add(bill)
        db.session.commit()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, bill.invoice_pdf) if bill.invoice_pdf else None
    
    if not full_path or not os.path.exists(full_path):
        from utils.pdf_generator import generate_invoice_pdf
        rel_path = generate_invoice_pdf(bill)
        bill.invoice_pdf = rel_path
        db.session.commit()
        full_path = os.path.join(base_dir, rel_path)

    return send_file(
        full_path,
        mimetype='application/pdf',
        as_attachment=False,
        download_name=f"VisionEdge_Invoice_{bill.invoice_number}.pdf"
    )
