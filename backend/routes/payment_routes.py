from flask import Blueprint, request, jsonify, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import (db, Order, OrderItem, Billing, Payment,
                    Customer, Frame, Lens, User, OrderStatusHistory)
from routes.billing_routes import generate_invoice_number
from routes.order_routes import generate_order_number
import hashlib
import uuid
import os
from datetime import datetime

payment_bp = Blueprint('payment', __name__)

# ---------------------------------------------------------------------------
# PayU Config  (TEST credentials — replace with live keys via .env)
# ---------------------------------------------------------------------------
PAYU_KEY  = os.environ.get('PAYU_KEY', '').strip()
PAYU_SALT = os.environ.get('PAYU_SALT', '').strip()
PAYU_URL  = os.environ.get('PAYU_URL',  'https://test.payu.in/_payment')
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:8000')


# ---------------------------------------------------------------------------
# Hash Helpers
# ---------------------------------------------------------------------------
def generate_payu_hash(key, txnid, amount, productinfo, firstname, email,
                       udf1='', udf2='', udf3='', udf4='', udf5='', salt=''):
    """SHA-512 forward hash for initiating a PayU transaction."""
    s = (f"{key}|{txnid}|{amount}|{productinfo}|{firstname}|{email}"
         f"|{udf1}|{udf2}|{udf3}|{udf4}|{udf5}||||||{salt}")
    return hashlib.sha512(s.encode('utf-8')).hexdigest()


def verify_payu_hash(data: dict, salt: str) -> bool:
    """Verify the reverse hash returned by PayU in the callback."""
    status      = data.get('status', '')
    key         = data.get('key', '')
    txnid       = data.get('txnid', '')
    amount      = data.get('amount', '')
    productinfo = data.get('productinfo', '')
    firstname   = data.get('firstname', '')
    email       = data.get('email', '')
    udf1        = data.get('udf1', '')
    udf2        = data.get('udf2', '')
    udf3        = data.get('udf3', '')
    udf4        = data.get('udf4', '')
    udf5        = data.get('udf5', '')
    hash_from_payu = data.get('hash', '')

    # Reverse hash: SALT|status||||||udf5|...|udf1|email|firstname|productinfo|amount|txnid|key
    s = (f"{salt}|{status}||||||{udf5}|{udf4}|{udf3}|{udf2}|{udf1}"
         f"|{email}|{firstname}|{productinfo}|{amount}|{txnid}|{key}")
    computed = hashlib.sha512(s.encode('utf-8')).hexdigest()
    return computed == hash_from_payu


# ---------------------------------------------------------------------------
# 1. Initiate Payment
# ---------------------------------------------------------------------------
@payment_bp.route('/initiate', methods=['POST'])
@jwt_required()
def initiate_payment():
    """
    Called by the frontend checkout page.
    Creates a pending Order + Billing record and returns the PayU params
    (including the hash) so the frontend can submit the payment form to PayU.
    """
    if not PAYU_KEY or not PAYU_SALT:
        return jsonify({"message": "PayU payments are not configured."}), 503

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json or {}

    if not data.get('items'):
        return jsonify({"message": "Cart items are required"}), 400

    try:
        # ---- Resolve or create Customer record ----
        customer = Customer.query.filter_by(created_by=user.id).first()
        if not customer:
            customer = Customer.query.filter_by(phone=user.phone).first() if user.phone else None
        if not customer and user.email:
            customer = Customer.query.filter_by(email=user.email).first()
        if not customer:
            last_c = Customer.query.order_by(Customer.id.desc()).first()
            next_id = (last_c.id + 1) if last_c else 1
            customer = Customer(
                customer_code=f"CUST{next_id:04d}",
                first_name=user.first_name or user.username,
                last_name=user.last_name or '',
                phone=user.phone or data.get('phone', '0000000000'),
                email=user.email,
                address=data.get('shipping_address', ''),
                created_by=user.id
            )
            db.session.add(customer)
            db.session.flush()

        # ---- Create pending Order ----
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
            item_id   = item_data['item_id']
            qty       = int(item_data['quantity'])

            product = Frame.query.get(item_id) if item_type == 'Frame' else Lens.query.get(item_id)

            if not product:
                db.session.rollback()
                return jsonify({"message": f"{item_type} with id={item_id} not found"}), 404

            if product.stock < qty:
                db.session.rollback()
                return jsonify({"message": f"Insufficient stock for {product.name}"}), 400

            price_val  = (product.selling_price
                          if hasattr(product, 'selling_price') and product.selling_price is not None
                          else product.price)
            unit_price = float(price_val or 0)
            item_sub   = unit_price * qty
            gst_perc   = getattr(product, 'gst_percent', 0.0) or 0.0
            item_gst   = item_sub * (gst_perc / 100.0)
            item_total = item_sub + item_gst

            subtotal  += item_sub
            gst_total += item_gst

            db.session.add(OrderItem(
                order_id=order.id,
                item_type=item_type,
                item_id=item_id,
                quantity=qty,
                unit_price=unit_price,
                total_price=item_total
            ))

        discount_val = float(data.get('discount', 0.0) or 0.0)
        order.subtotal    = subtotal
        order.discount    = discount_val
        order.gst         = gst_total
        order.total_amount = max(0.0, subtotal + gst_total - discount_val)

        # ---- Generate unique PayU transaction ID ----
        txnid = f"VE-{uuid.uuid4().hex[:12].upper()}"

        # ---- Create Pending Billing record ----
        invoice_number = generate_invoice_number()
        billing = Billing(
            invoice_number=invoice_number,
            order_id=order.id,
            subtotal=subtotal,
            discount=discount_val,
            gst=gst_total,
            total_amount=order.total_amount,
            payment_method=f'PayU|{txnid}',
            payment_status='Pending'
        )
        db.session.add(billing)
        db.session.flush()

        db.session.add(OrderStatusHistory(
            order_id=order.id,
            status='Pending',
            notes=f'Payment initiated via PayU. TxnID: {txnid}'
        ))
        db.session.commit()

        # ---- Build PayU params ----
        amount_str  = f"{order.total_amount:.2f}"
        firstname   = (user.first_name or user.username or 'Customer').strip()
        email_val   = user.email or f"{user.username}@visionedge.com"
        productinfo = f"VisionEdge Order {ord_num}"

        hash_val = generate_payu_hash(
            key=PAYU_KEY,
            txnid=txnid,
            amount=amount_str,
            productinfo=productinfo,
            firstname=firstname,
            email=email_val,
            udf1=str(order.id),
            udf2=str(billing.id),
            salt=PAYU_SALT
        )

        base = request.host_url.rstrip('/')
        if ':5000' not in base and ':8000' not in base:
            base = 'http://127.0.0.1:5000'
        surl = f"{base}/api/payment/payu/success"
        furl = f"{base}/api/payment/payu/failure"

        return jsonify({
            "payu_url":         PAYU_URL,
            "key":              PAYU_KEY,
            "txnid":            txnid,
            "amount":           amount_str,
            "productinfo":      productinfo,
            "firstname":        firstname,
            "email":            email_val,
            "phone":            user.phone or data.get('phone', ''),
            "surl":             surl,
            "furl":             furl,
            "hash":             hash_val,
            "udf1":             str(order.id),
            "udf2":             str(billing.id),
            "service_provider": "payu_paisa",
            "order_id":         order.id,
            "billing_id":       billing.id,
            "invoice_number":   invoice_number,
            "order_number":     ord_num,
            "total_amount":     order.total_amount
        }), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        err_detail = traceback.format_exc()
        print("=== PAYMENT INITIATE ERROR ===")
        print(err_detail)
        return jsonify({"message": f"Failed to initiate payment: {str(e)}", "detail": err_detail}), 500



# ---------------------------------------------------------------------------
# 2. PayU Success Callback
# ---------------------------------------------------------------------------
@payment_bp.route('/payu/success', methods=['POST'])
def payu_success():
    form = request.form.to_dict()

    if not verify_payu_hash(form, PAYU_SALT):
        return redirect(
            f"{FRONTEND_URL}/payment-failed.html"
            f"?reason=hash_mismatch&txnid={form.get('txnid','')}"
        )

    txnid       = form.get('txnid', '')
    payu_txnid  = form.get('mihpayid', txnid)
    amount      = form.get('amount', '0')
    order_id    = form.get('udf1', '')
    billing_id  = form.get('udf2', '')

    try:
        billing = Billing.query.get(int(billing_id)) if billing_id else None
        if billing:
            billing.payment_status = 'Paid'
            billing.payment_method = 'PayU'

            db.session.add(Payment(
                billing_id=billing.id,
                amount=float(amount),
                payment_method='PayU',
                transaction_id=payu_txnid
            ))

            if order_id:
                order = Order.query.get(int(order_id))
                if order and order.status == 'Pending':
                    order.status = 'Confirmed'
                    db.session.add(OrderStatusHistory(
                        order_id=order.id,
                        status='Confirmed',
                        notes=f'Payment confirmed via PayU. MihPayID: {payu_txnid}'
                    ))

        db.session.commit()

        invoice = billing.invoice_number if billing else ''
        return redirect(
            f"{FRONTEND_URL}/payment-success.html"
            f"?txnid={payu_txnid}&order={order_id}&invoice={invoice}&amount={amount}"
        )

    except Exception:
        db.session.rollback()
        import traceback; traceback.print_exc()
        return redirect(
            f"{FRONTEND_URL}/payment-failed.html?reason=server_error&txnid={txnid}"
        )


# ---------------------------------------------------------------------------
# 3. PayU Failure Callback
# ---------------------------------------------------------------------------
@payment_bp.route('/payu/failure', methods=['POST'])
def payu_failure():
    form = request.form.to_dict()

    txnid      = form.get('txnid', '')
    order_id   = form.get('udf1', '')
    billing_id = form.get('udf2', '')
    reason     = form.get('error_Message', form.get('error', 'Payment failed or cancelled'))

    try:
        billing = Billing.query.get(int(billing_id)) if billing_id else None
        if billing:
            billing.payment_status = 'Failed'
            billing.payment_method = 'PayU'

            if order_id:
                order = Order.query.get(int(order_id))
                if order and order.status == 'Pending':
                    order.status = 'Cancelled'
                    db.session.add(OrderStatusHistory(
                        order_id=order.id,
                        status='Cancelled',
                        notes=f'Payment failed via PayU. TxnID: {txnid}. Reason: {reason}'
                    ))

        db.session.commit()

    except Exception:
        db.session.rollback()

    import urllib.parse
    return redirect(
        f"{FRONTEND_URL}/payment-failed.html"
        f"?txnid={txnid}&reason={urllib.parse.quote(str(reason))}"
    )


# ---------------------------------------------------------------------------
# 4. Payment Status Check (JWT-protected)
# ---------------------------------------------------------------------------
@payment_bp.route('/status/<txnid>', methods=['GET'])
@jwt_required()
def check_payment_status(txnid):
    billing = Billing.query.filter(Billing.payment_method.like(f'%{txnid}%')).first()
    if not billing:
        pmt = Payment.query.filter_by(transaction_id=txnid).first()
        if pmt:
            billing = Billing.query.get(pmt.billing_id)

    if not billing:
        return jsonify({"message": "Transaction not found"}), 404

    return jsonify({
        "txnid":          txnid,
        "status":         billing.payment_status,
        "amount":         billing.total_amount,
        "invoice_number": billing.invoice_number,
        "order_id":       billing.order_id
    }), 200


# ---------------------------------------------------------------------------
# 5. My Orders (customer-facing)
# ---------------------------------------------------------------------------
@payment_bp.route('/my-orders', methods=['GET'])
@jwt_required()
def my_orders():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Resolve customer: by created_by, then phone, then email
    customer = Customer.query.filter_by(created_by=user.id).first()
    if not customer and user.phone:
        customer = Customer.query.filter_by(phone=user.phone).first()
    if not customer and user.email:
        customer = Customer.query.filter_by(email=user.email).first()
    if not customer:
        return jsonify([]), 200

    orders = (Order.query
              .filter_by(customer_id=customer.id)
              .order_by(Order.created_at.desc())
              .all())

    result = []
    for o in orders:
        b = o.billing
        pm_display = None
        if b and b.payment_method:
            pm_display = b.payment_method.split('|')[0]
        p = o.order_payments[-1] if (hasattr(o, 'order_payments') and o.order_payments) else (b.payments[0] if (b and hasattr(b, 'payments') and b.payments) else None)
        result.append({
            "order_id":       o.id,
            "order_number":   o.order_number or o.order_id,
            "status":         o.status,
            "total_amount":   float(o.total_amount or 0),
            "created_at":     str(o.created_at),
            "invoice_number": b.invoice_number if b else None,
            "payment_status": b.payment_status if b else 'Pending',
            "payment_method": p.payment_method if (p and p.payment_method) else (pm_display or 'Razorpay'),
            "transaction_id": (p.gateway_payment_id or p.transaction_id) if p else None,
            "gateway":        p.gateway if p else "Razorpay",
            "gateway_status": p.gateway_status if p else (b.payment_status if b else 'Pending'),
            "refund_status":  p.refund_status if p else None,
            "refunded_amount": float(p.refunded_amount or 0.0) if p else 0.0,
            "billing_id":     b.id if b else None,
        })

    return jsonify(result), 200


# ---------------------------------------------------------------------------
# 6. My Payment History — detailed billing records (customer-facing)
# ---------------------------------------------------------------------------
@payment_bp.route('/my-history', methods=['GET'])
@jwt_required()
def my_payment_history():
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
        return jsonify([]), 200

    # Get all billings for this customer's orders
    billings = (db.session.query(Billing)
                .join(Order, Billing.order_id == Order.id)
                .filter(Order.customer_id == customer.id)
                .order_by(Billing.created_at.desc())
                .all())

    result = []
    for b in billings:
        o = b.order_rel or Order.query.get(b.order_id)
        p = b.payments[0] if (hasattr(b, 'payments') and b.payments) else Payment.query.filter_by(order_id=b.order_id).order_by(Payment.id.desc()).first()
        result.append({
            "billing_id":     b.id,
            "invoice_number": b.invoice_number,
            "order_number":   o.order_number if o else None,
            "order_id":       b.order_id,
            "subtotal":       float(b.subtotal or 0),
            "gst":            float(b.gst or 0),
            "discount":       float(b.discount or 0),
            "total_amount":   float(b.total_amount or 0),
            "payment_method": (p.payment_method if (p and p.payment_method) else (b.payment_method or '')).split('|')[0],
            "payment_status": b.payment_status,
            "transaction_id": (p.gateway_payment_id or p.transaction_id) if p else None,
            "gateway":        p.gateway if p else "Razorpay",
            "gateway_status": p.gateway_status if p else b.payment_status,
            "refund_status":  p.refund_status if p else None,
            "refunded_amount": float(p.refunded_amount or 0.0) if p else 0.0,
            "created_at":     str(b.created_at),
            "has_pdf":        bool(b.invoice_pdf),
        })

    return jsonify(result), 200
