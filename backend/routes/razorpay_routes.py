"""
VisionEdge — Razorpay Payment Gateway Routes
============================================
Handles:
  - Configuration retrieval (Public Key ID only)
  - Order creation with authoritative server-side price & coupon recalculation
  - Payment signature verification and instant order fulfillment
  - Webhook processing with replay protection & signature validation
  - Real-time verified order and payment status checking
  - Retry payment generation for failed/pending orders
  - Admin refunds (full and partial)
  - Admin transaction metrics & listings
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Tuple

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from config import Config
from models import (
    db, Order, OrderItem, Billing, Payment, Customer,
    Frame, Lens, User, OrderStatusHistory, WebhookEvent
)
from services.razorpay_service import RazorpayService
from routes.billing_routes import generate_invoice_number
from routes.order_routes import generate_order_number

logger = logging.getLogger("visionedge.razorpay_routes")

razorpay_bp = Blueprint("razorpay", __name__)


# ---------------------------------------------------------------------------
# Helper: Authoritative Discount Recalculation
# ---------------------------------------------------------------------------
def calculate_authoritative_discount(coupon_code: str, subtotal: float) -> float:
    """
    Recalculate discount strictly server-side.
    Supported coupons:
      - VISION30: 30% discount
      - BOGO2026: 50% discount
      - STUDENT15: 15% discount
      - FREESHIP: flat ₹100 discount
    """
    if not coupon_code or not subtotal or subtotal <= 0:
        return 0.0

    code = str(coupon_code).strip().upper()
    if code == "VISION30":
        return round(subtotal * 0.30, 2)
    elif code == "BOGO2026":
        return round(subtotal * 0.50, 2)
    elif code == "STUDENT15":
        return round(subtotal * 0.15, 2)
    elif code == "FREESHIP":
        return min(round(subtotal, 2), 100.0)

    return 0.0


# ---------------------------------------------------------------------------
# 1. GET /config — Public Configuration
# ---------------------------------------------------------------------------
@razorpay_bp.route("/config", methods=["GET"])
def get_razorpay_config():
    """
    Returns public key ID and mode for frontend Razorpay checkout.
    Never exposes RAZORPAY_KEY_SECRET or webhook secret.
    """
    return jsonify({
        "configured": RazorpayService.is_configured(),
        "key_id": Config.RAZORPAY_KEY_ID or "",
        "currency": Config.RAZORPAY_CURRENCY or "INR",
        "mode": Config.RAZORPAY_MODE or "test",
        "business_name": "VisionEdge Opticals",
        "description": "Smart Optical Store & Eyewear"
    }), 200


# ---------------------------------------------------------------------------
# 2. POST /create-order — Server-Side Authoritative Order Creation
# ---------------------------------------------------------------------------
@razorpay_bp.route("/create-order", methods=["POST"])
@jwt_required()
def create_razorpay_order():
    """
    Authoritative order initiation:
      1. Validates authenticated user.
      2. Validates item existence and stock against database.
      3. Recalculates subtotal, GST (18%), and authoritative coupon discount.
      4. Creates internal Order (Pending) and Billing (Pending).
      5. Calls Razorpay API to generate razorpay_order_id.
      6. Creates Payment record in 'created' state.
      7. Returns order metadata to frontend.
    """
    if not RazorpayService.is_configured():
        return jsonify({
            "message": "Online payment is currently unavailable. Razorpay is not configured."
        }), 503

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json(silent=True) or {}
    items_data = data.get("items")
    if not items_data or not isinstance(items_data, list):
        return jsonify({"message": "Items array is required"}), 400

    try:
        # Update user profile details from checkout input if provided
        phone_input = (data.get("phone") or "").strip()
        address_input = (data.get("shipping_address") or "").strip()
        first_name_input = (data.get("first_name") or "").strip()
        last_name_input = (data.get("last_name") or "").strip()

        if phone_input:
            user.phone = phone_input
        if address_input:
            user.address = address_input
        if first_name_input and not user.first_name:
            user.first_name = first_name_input
        if last_name_input and not user.last_name:
            user.last_name = last_name_input

        # Find or create customer record
        customer = Customer.query.filter_by(created_by=user.id).first()
        if not customer:
            if user.phone:
                customer = Customer.query.filter_by(phone=user.phone).first()
            if not customer and user.email:
                customer = Customer.query.filter_by(email=user.email).first()

            if not customer:
                last_customer = Customer.query.order_by(Customer.id.desc()).first()
                next_id = (last_customer.id + 1) if last_customer else 1
                customer = Customer(
                    customer_code=f"CUST{next_id:04d}",
                    first_name=user.first_name or user.username,
                    last_name=user.last_name or "",
                    phone=phone_input or user.phone or "0000000000",
                    email=user.email,
                    address=address_input or user.address or "",
                    created_by=user.id
                )
                db.session.add(customer)
                db.session.flush()

        if customer:
            if phone_input:
                customer.phone = phone_input
            if address_input:
                customer.address = address_input
            if first_name_input and not customer.first_name:
                customer.first_name = first_name_input
            if last_name_input and not customer.last_name:
                customer.last_name = last_name_input

        # Recalculate totals strictly from database
        subtotal = 0.0
        gst_total = 0.0
        validated_items = []

        for item_entry in items_data:
            itype = str(item_entry.get("item_type") or item_entry.get("product_type") or "Frame").strip()
            raw_id = item_entry.get("item_id") or item_entry.get("product_id") or item_entry.get("id")
            try:
                iid = int(raw_id)
            except (ValueError, TypeError):
                iid = raw_id

            try:
                qty = int(item_entry.get("quantity", 1))
            except (ValueError, TypeError):
                qty = 1

            if qty <= 0:
                continue

            if itype.lower() == "lens":
                product = Lens.query.get(iid)
                prod_type = "Lens"
            else:
                product = Frame.query.get(iid)
                prod_type = "Frame"

            if not product:
                return jsonify({"message": f"{prod_type} with ID {iid} not found"}), 404

            if product.stock < qty:
                return jsonify({
                    "message": f"Insufficient stock for '{product.name}'. Available: {product.stock}, Requested: {qty}"
                }), 400

            # Price lookup
            price_val = getattr(product, "selling_price", None)
            if price_val is None:
                price_val = getattr(product, "price", 0.0)
            unit_price = float(price_val or 0.0)

            item_subtotal = round(unit_price * qty, 2)
            # Retail selling prices are tax-inclusive by standard; fallback gst_percent is 0.0 unless set
            gst_perc = float(getattr(product, "gst_percent", 0.0) or 0.0)
            item_gst = round(item_subtotal * (gst_perc / 100.0), 2) if gst_perc > 0 else 0.0
            item_total = item_subtotal + item_gst

            subtotal += item_subtotal
            gst_total += item_gst

            validated_items.append({
                "item_type": prod_type,
                "item_id": product.id,
                "name": product.name,
                "quantity": qty,
                "unit_price": unit_price,
                "total_price": item_total
            })

        if not validated_items:
            return jsonify({"message": "No valid items in cart"}), 400

        subtotal = round(subtotal, 2)
        gst_total = round(gst_total, 2)

        # Coupon code validation
        coupon_code = (data.get("coupon_code") or "").strip()
        discount_val = calculate_authoritative_discount(coupon_code, subtotal)

        final_amount = max(1.0, round(subtotal + gst_total - discount_val, 2))

        # Generate internal Order
        ord_num = generate_order_number()
        order = Order(
            order_id=ord_num,
            order_number=ord_num,
            customer_id=customer.id,
            prescription_id=data.get("prescription_id"),
            status="Pending",
            subtotal=subtotal,
            gst=gst_total,
            discount=discount_val,
            total_amount=final_amount,
            notes=f"Online order via Razorpay. Coupon: {coupon_code or 'None'}"
        )
        db.session.add(order)
        db.session.flush()

        # Add OrderItems
        for v_item in validated_items:
            order_item = OrderItem(
                order_id=order.id,
                item_type=v_item["item_type"],
                item_id=v_item["item_id"],
                quantity=v_item["quantity"],
                unit_price=v_item["unit_price"],
                total_price=v_item["total_price"]
            )
            db.session.add(order_item)

        # Generate internal Billing record
        inv_num = generate_invoice_number()
        billing = Billing(
            invoice_number=inv_num,
            order_id=order.id,
            subtotal=subtotal,
            discount=discount_val,
            gst=gst_total,
            total_amount=final_amount,
            payment_method="Razorpay",
            payment_status="Pending"
        )
        db.session.add(billing)
        db.session.flush()

        # Create Razorpay order
        notes = {
            "order_id": str(order.id),
            "order_number": order.order_number,
            "invoice_number": inv_num,
            "customer_id": str(customer.id),
            "customer_email": user.email or "",
            "store": "VisionEdge Opticals"
        }
        rzp_order = RazorpayService.create_order(
            amount_in_rupees=final_amount,
            receipt=order.order_number,
            notes=notes,
            currency=Config.RAZORPAY_CURRENCY or "INR"
        )
        rzp_order_id = rzp_order.get("id")

        # Create tracking Payment record
        payment = Payment(
            billing_id=billing.id,
            order_id=order.id,
            amount=final_amount,
            currency=Config.RAZORPAY_CURRENCY or "INR",
            payment_method="Razorpay",
            gateway="Razorpay",
            gateway_order_id=rzp_order_id,
            gateway_status="created",
            signature_verified=False
        )
        db.session.add(payment)

        # Order status history
        history = OrderStatusHistory(
            order_id=order.id,
            status="Pending",
            notes=f"Payment initiated via Razorpay (Order ID: {rzp_order_id}). Amount: ₹{final_amount:.2f}"
        )
        db.session.add(history)

        db.session.commit()

        customer_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or user.username
        return jsonify({
            "status": "success",
            "razorpay_order_id": rzp_order_id,
            "amount": rzp_order.get("amount"),  # in paise
            "currency": rzp_order.get("currency", "INR"),
            "key_id": Config.RAZORPAY_KEY_ID,
            "order_id": order.id,
            "order_number": order.order_number,
            "invoice_number": billing.invoice_number,
            "billing_id": billing.id,
            "subtotal": subtotal,
            "gst": gst_total,
            "discount": discount_val,
            "total_amount": final_amount,
            "customer": {
                "name": customer_name,
                "email": user.email or "",
                "phone": customer.phone or user.phone or ""
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.exception("Error in create_razorpay_order: %s", str(e))
        return jsonify({"message": f"Failed to initiate Razorpay order: {str(e)}"}), 500


# ---------------------------------------------------------------------------
# 3. POST /verify — Signature & Gateway Verification and Fulfillment
# ---------------------------------------------------------------------------
@razorpay_bp.route("/verify", methods=["POST"])
@jwt_required()
def verify_razorpay_payment():
    """
    Verifies payment:
      1. Verifies HMAC-SHA256 signature.
      2. Validates against duplicate/replay attacks.
      3. Fetches live payment status from Razorpay API.
      4. Marks Payment captured, Billing Paid, Order Confirmed.
      5. Generates invoice PDF.
    """
    data = request.get_json(silent=True) or {}
    rzp_order_id = data.get("razorpay_order_id")
    rzp_payment_id = data.get("razorpay_payment_id")
    rzp_signature = data.get("razorpay_signature")

    if not rzp_order_id or not rzp_payment_id or not rzp_signature:
        return jsonify({
            "status": "failed",
            "message": "Missing required Razorpay payment credentials (order_id, payment_id, signature)."
        }), 400

    # Locate tracking Payment record
    payment = Payment.query.filter_by(gateway_order_id=rzp_order_id).order_by(Payment.id.desc()).first()
    if not payment:
        return jsonify({
            "status": "failed",
            "message": f"No local transaction found matching Razorpay order ID '{rzp_order_id}'."
        }), 404

    # Idempotency check: Already verified
    if payment.signature_verified and payment.gateway_status in ("captured", "authorized"):
        order = payment.order_rel or (payment.billing.order_rel if payment.billing else None)
        return jsonify({
            "status": "success",
            "message": "Payment has already been verified.",
            "order_id": order.id if order else payment.order_id,
            "order_number": order.order_number if order else None,
            "invoice_number": payment.billing.invoice_number if payment.billing else None,
            "transaction_id": payment.gateway_payment_id or payment.transaction_id,
            "amount": float(payment.amount),
            "payment_status": "Paid",
            "payment_method": "Razorpay"
        }), 200

    # 1. Verify Signature
    is_valid_sig, sig_err = RazorpayService.verify_payment_signature(
        razorpay_order_id=rzp_order_id,
        razorpay_payment_id=rzp_payment_id,
        razorpay_signature=rzp_signature
    )

    if not is_valid_sig:
        payment.gateway_status = "failed"
        payment.failure_code = "INVALID_SIGNATURE"
        payment.failure_reason = sig_err or "HMAC signature mismatch"
        payment.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({
            "status": "failed",
            "message": "Payment signature verification failed. Transaction cannot be confirmed."
        }), 400

    # 2. Fetch live payment from Razorpay API
    try:
        rzp_payment_data = RazorpayService.fetch_payment(rzp_payment_id)
    except Exception as e:
        logger.error("Failed to fetch payment %s from Razorpay: %s", rzp_payment_id, str(e))
        return jsonify({
            "status": "failed",
            "message": "Unable to verify payment status with payment gateway."
        }), 502

    rzp_status = rzp_payment_data.get("status")
    rzp_amount_paise = rzp_payment_data.get("amount", 0)
    expected_paise = RazorpayService.rupees_to_paise(payment.amount)

    # Validate amount
    if abs(rzp_amount_paise - expected_paise) > 100:  # Allow max ₹1 rounding difference
        payment.gateway_status = "failed"
        payment.failure_code = "AMOUNT_MISMATCH"
        payment.failure_reason = (
            f"Expected {expected_paise} paise, received {rzp_amount_paise} paise."
        )
        db.session.commit()
        return jsonify({
            "status": "failed",
            "message": "Payment amount mismatch between merchant and gateway."
        }), 400

    if rzp_status not in ("captured", "authorized"):
        payment.gateway_status = rzp_status or "failed"
        payment.failure_code = rzp_payment_data.get("error_code") or "NOT_CAPTURED"
        payment.failure_reason = rzp_payment_data.get("error_description") or f"Payment status is {rzp_status}"
        db.session.commit()
        return jsonify({
            "status": "failed",
            "message": f"Payment was not successfully captured. Gateway status: {rzp_status}"
        }), 400

    # 3. Successful Verification & Database Updates
    now = datetime.utcnow()
    payment.gateway_payment_id = rzp_payment_id
    payment.gateway_signature = rzp_signature
    payment.gateway_status = "captured"
    payment.signature_verified = True
    payment.transaction_id = rzp_payment_id
    payment.payment_method = "Razorpay"
    payment.paid_at = now
    payment.updated_at = now
    payment.raw_response = json.dumps(rzp_payment_data)

    order = payment.order_rel or (payment.billing.order_rel if payment.billing else None)
    billing = payment.billing or (order.billing if order else None)

    if billing:
        billing.payment_status = "Paid"
        billing.payment_method = "Razorpay"

    if order:
        order.status = "Confirmed"

        # Record Order Status History
        history = OrderStatusHistory(
            order_id=order.id,
            status="Confirmed",
            notes=f"Payment verified successfully via Razorpay (Txn: {rzp_payment_id}). Status: Paid."
        )
        db.session.add(history)

    # Generate Invoice PDF if possible
    try:
        from utils.pdf_generator import generate_invoice_pdf
        if billing and order:
            customer = order.customer
            order_items = [
                {
                    "product_name": getattr(item, "product_name", None) or f"Item #{item.item_id}",
                    "item_type": getattr(item, "item_type", "Product"),
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total_price": item.total_price
                }
                for item in order.items
            ]
            pdf_path = generate_invoice_pdf(billing, order_items, customer)
            billing.invoice_pdf = pdf_path
    except Exception as pdf_err:
        logger.warning("Could not auto-generate PDF invoice on verify: %s", str(pdf_err))

    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Payment verified and order confirmed successfully.",
        "order_id": order.id if order else payment.order_id,
        "order_number": order.order_number if order else None,
        "invoice_number": billing.invoice_number if billing else None,
        "transaction_id": rzp_payment_id,
        "amount": float(payment.amount),
        "payment_status": "Paid",
        "payment_method": "Razorpay"
    }), 200


# ---------------------------------------------------------------------------
# 4. POST /webhook — Secure Asynchronous Webhook Handler
# ---------------------------------------------------------------------------
@razorpay_bp.route("/webhook", methods=["POST"])
def handle_razorpay_webhook():
    """
    Authoritative webhook listener:
      - Validates X-Razorpay-Signature HMAC using raw request bytes.
      - Implements idempotent deduplication via WebhookEvent model.
      - Handles payment.captured, payment.failed, refund.created, refund.processed.
    """
    raw_body = request.get_data()
    webhook_signature = request.headers.get("X-Razorpay-Signature", "")

    if not webhook_signature:
        logger.warning("Webhook received without X-Razorpay-Signature header.")
        return jsonify({"message": "Missing webhook signature"}), 400

    # Signature validation
    is_valid, err_msg = RazorpayService.verify_webhook_signature(
        raw_body=raw_body,
        webhook_signature=webhook_signature
    )
    if not is_valid:
        logger.error("Razorpay webhook signature verification failed: %s", err_msg)
        return jsonify({"message": "Invalid webhook signature"}), 400

    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except Exception as e:
        return jsonify({"message": "Invalid JSON body"}), 400

    event_id = payload.get("id") or payload.get("event_id")
    event_type = payload.get("event")

    if not event_id or not event_type:
        return jsonify({"message": "Missing event ID or event type"}), 400

    # Deduplication check
    existing_event = WebhookEvent.query.filter_by(event_id=event_id).first()
    if existing_event and existing_event.status == "processed":
        logger.info("Webhook event %s already processed. Skipping.", event_id)
        return jsonify({"status": "already_processed"}), 200

    if not existing_event:
        existing_event = WebhookEvent(
            gateway="Razorpay",
            event_id=event_id,
            event_type=event_type,
            payload=json.dumps(payload),
            status="pending"
        )
        db.session.add(existing_event)
        db.session.commit()

    # Process events
    try:
        event_payload = payload.get("payload", {})

        if event_type == "payment.captured":
            payment_entity = event_payload.get("payment", {}).get("entity", {})
            rzp_payment_id = payment_entity.get("id")
            rzp_order_id = payment_entity.get("order_id")

            payment = None
            if rzp_order_id:
                payment = Payment.query.filter_by(gateway_order_id=rzp_order_id).order_by(Payment.id.desc()).first()
            if not payment and rzp_payment_id:
                payment = Payment.query.filter_by(gateway_payment_id=rzp_payment_id).first()

            if payment and payment.gateway_status != "captured":
                payment.gateway_payment_id = rzp_payment_id
                payment.gateway_status = "captured"
                payment.signature_verified = True
                payment.transaction_id = rzp_payment_id
                payment.paid_at = datetime.utcnow()
                payment.updated_at = datetime.utcnow()

                order = payment.order_rel or (payment.billing.order_rel if payment.billing else None)
                billing = payment.billing or (order.billing if order else None)
                if billing:
                    billing.payment_status = "Paid"
                    billing.payment_method = "Razorpay"
                if order and order.status != "Confirmed":
                    order.status = "Confirmed"
                    history = OrderStatusHistory(
                        order_id=order.id,
                        status="Confirmed",
                        notes=f"Confirmed via Razorpay Webhook ({event_id}). Payment: {rzp_payment_id}"
                    )
                    db.session.add(history)

        elif event_type == "payment.failed":
            payment_entity = event_payload.get("payment", {}).get("entity", {})
            rzp_payment_id = payment_entity.get("id")
            rzp_order_id = payment_entity.get("order_id")

            payment = None
            if rzp_order_id:
                payment = Payment.query.filter_by(gateway_order_id=rzp_order_id).order_by(Payment.id.desc()).first()
            if payment:
                payment.gateway_status = "failed"
                payment.failure_code = payment_entity.get("error_code")
                payment.failure_reason = payment_entity.get("error_description")
                payment.updated_at = datetime.utcnow()

        elif event_type in ("refund.created", "refund.processed"):
            refund_entity = event_payload.get("refund", {}).get("entity", {})
            rzp_payment_id = refund_entity.get("payment_id")
            refund_id = refund_entity.get("id")
            refund_amount_paise = refund_entity.get("amount", 0)
            refund_amount_rupees = RazorpayService.paise_to_rupees(refund_amount_paise)

            payment = Payment.query.filter_by(gateway_payment_id=rzp_payment_id).first()
            if payment:
                payment.refund_id = refund_id
                current_refunded = float(payment.refunded_amount or 0.0)
                new_refunded = round(current_refunded + refund_amount_rupees, 2)
                payment.refunded_amount = new_refunded
                payment.refund_status = "full" if new_refunded >= float(payment.amount) else "partial"
                payment.updated_at = datetime.utcnow()

                order = payment.order_rel or (payment.billing.order_rel if payment.billing else None)
                billing = payment.billing or (order.billing if order else None)

                if payment.refund_status == "full":
                    if billing:
                        billing.payment_status = "Refunded"
                    if order:
                        order.status = "Refunded"
                        history = OrderStatusHistory(
                            order_id=order.id,
                            status="Refunded",
                            notes=f"Full refund of ₹{new_refunded:.2f} processed via Razorpay Webhook ({refund_id})."
                        )
                        db.session.add(history)

        existing_event.status = "processed"
        existing_event.processed_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"status": "success", "event_id": event_id}), 200

    except Exception as e:
        db.session.rollback()
        logger.exception("Error processing webhook %s: %s", event_id, str(e))
        existing_event.status = "failed"
        existing_event.error_message = str(e)
        existing_event.processed_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "Webhook processing encountered an error"}), 500


# ---------------------------------------------------------------------------
# 5. GET /status/<order_id_or_number> — Authoritative Verified Status
# ---------------------------------------------------------------------------
@razorpay_bp.route("/status/<order_id_or_number>", methods=["GET"])
@jwt_required()
def get_order_payment_status(order_id_or_number):
    """
    Returns authoritative payment and order details from the database.
    Used by payment-success.html and payment-failed.html.
    Prevents trusting frontend URL query parameters.
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Resolve order
    order = None
    if str(order_id_or_number).isdigit():
        order = Order.query.get(int(order_id_or_number))
    if not order:
        order = Order.query.filter(
            (Order.order_number == order_id_or_number) | (Order.order_id == order_id_or_number)
        ).first()

    if not order:
        return jsonify({"message": "Order not found"}), 404

    # Authorization check: Owner or Admin/Staff
    is_admin_or_staff = (user.role or "").lower() in ("admin", "staff")
    is_owner = False
    if order.customer:
        if order.customer.created_by == user.id or (user.email and order.customer.email == user.email):
            is_owner = True

    if not is_admin_or_staff and not is_owner:
        return jsonify({"message": "You do not have permission to view this order"}), 403

    payment = Payment.query.filter_by(order_id=order.id).order_by(Payment.id.desc()).first()
    if not payment and order.billing:
        payment = Payment.query.filter_by(billing_id=order.billing.id).order_by(Payment.id.desc()).first()

    billing = order.billing

    return jsonify({
        "order_id": order.id,
        "order_number": order.order_number or order.order_id,
        "order_status": order.status,
        "order_date": order.created_at.isoformat() if order.created_at else None,
        "subtotal": float(order.subtotal or 0.0),
        "gst": float(order.gst or 0.0),
        "discount": float(order.discount or 0.0),
        "total_amount": float(order.total_amount or 0.0),
        "payment": {
            "id": payment.id if payment else None,
            "status": payment.gateway_status if payment else (billing.payment_status if billing else "Pending"),
            "is_paid": (billing.payment_status == "Paid") if billing else False,
            "transaction_id": (payment.gateway_payment_id or payment.transaction_id) if payment else None,
            "gateway_order_id": payment.gateway_order_id if payment else None,
            "payment_method": payment.payment_method if payment else (billing.payment_method if billing else "Razorpay"),
            "amount": float(payment.amount) if payment else float(order.total_amount),
            "paid_at": payment.paid_at.isoformat() if (payment and payment.paid_at) else None,
            "failure_reason": payment.failure_reason if payment else None,
            "refund_status": payment.refund_status if payment else None,
            "refunded_amount": float(payment.refunded_amount or 0.0) if payment else 0.0
        },
        "billing": {
            "invoice_number": billing.invoice_number if billing else None,
            "invoice_pdf": billing.invoice_pdf if billing else None,
            "payment_status": billing.payment_status if billing else "Pending"
        },
        "customer": {
            "name": f"{order.customer.first_name} {order.customer.last_name}" if order.customer else user.username,
            "email": order.customer.email if order.customer else user.email,
            "phone": order.customer.phone if order.customer else user.phone,
            "address": order.customer.address if order.customer else user.address
        },
        "items": [
            {
                "id": item.id,
                "item_type": item.item_type,
                "item_id": item.item_id,
                "quantity": item.quantity,
                "unit_price": float(item.unit_price or 0.0),
                "total_price": float(item.total_price or 0.0)
            }
            for item in order.items
        ]
    }), 200


# ---------------------------------------------------------------------------
# 6. POST /retry — Retry Payment for Existing Pending/Failed Order
# ---------------------------------------------------------------------------
@razorpay_bp.route("/retry", methods=["POST"])
@jwt_required()
def retry_razorpay_payment():
    """
    Generates a new Razorpay order for an existing pending or failed order,
    allowing the customer to retry without needing to re-add items to the cart.
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json(silent=True) or {}
    order_id = data.get("order_id")
    if not order_id:
        return jsonify({"message": "Order ID is required"}), 400

    order = Order.query.get(order_id)
    if not order:
        order = Order.query.filter_by(order_number=str(order_id)).first()
    if not order:
        return jsonify({"message": "Order not found"}), 404

    # Permission check
    is_admin = (user.role or "").lower() in ("admin", "staff")
    is_owner = order.customer and (order.customer.created_by == user.id or order.customer.email == user.email)
    if not is_admin and not is_owner:
        return jsonify({"message": "Unauthorized access to order"}), 403

    if order.status in ("Confirmed", "Delivered", "Ready for Pickup"):
        return jsonify({"message": "Order is already paid and confirmed."}), 400

    billing = order.billing
    if not billing:
        billing = Billing(
            invoice_number=generate_invoice_number(),
            order_id=order.id,
            subtotal=float(order.subtotal or order.total_amount or 0.0),
            discount=float(order.discount or 0.0),
            gst=float(order.gst or 0.0),
            total_amount=float(order.total_amount or 0.0),
            payment_method="Razorpay",
            payment_status="Pending"
        )
        db.session.add(billing)
        db.session.flush()

    final_amount = float(order.total_amount)

    try:
        notes = {
            "order_id": str(order.id),
            "order_number": order.order_number,
            "invoice_number": billing.invoice_number,
            "store": "VisionEdge Opticals (Retry)"
        }
        rzp_order = RazorpayService.create_order(
            amount_in_rupees=final_amount,
            receipt=f"RETRY-{order.order_number}",
            notes=notes,
            currency=Config.RAZORPAY_CURRENCY or "INR"
        )
        rzp_order_id = rzp_order.get("id")

        # Create new Payment tracking entry
        payment = Payment(
            billing_id=billing.id if billing else None,
            order_id=order.id,
            amount=final_amount,
            currency=Config.RAZORPAY_CURRENCY or "INR",
            payment_method="Razorpay",
            gateway="Razorpay",
            gateway_order_id=rzp_order_id,
            gateway_status="created",
            signature_verified=False
        )
        db.session.add(payment)

        history = OrderStatusHistory(
            order_id=order.id,
            status=order.status,
            notes=f"Payment retry initiated (Razorpay Order: {rzp_order_id})."
        )
        db.session.add(history)
        db.session.commit()

        customer_name = f"{order.customer.first_name} {order.customer.last_name}" if order.customer else user.username
        return jsonify({
            "status": "success",
            "razorpay_order_id": rzp_order_id,
            "amount": rzp_order.get("amount"),
            "currency": rzp_order.get("currency", "INR"),
            "key_id": Config.RAZORPAY_KEY_ID,
            "order_id": order.id,
            "order_number": order.order_number,
            "total_amount": final_amount,
            "customer": {
                "name": customer_name,
                "email": order.customer.email if order.customer else user.email,
                "phone": order.customer.phone if order.customer else user.phone
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.exception("Error in retry_razorpay_payment: %s", str(e))
        return jsonify({"message": f"Retry initiation failed: {str(e)}"}), 500


# ---------------------------------------------------------------------------
# 7. POST /refund — Admin-Initiated Refund Processing
# ---------------------------------------------------------------------------
@razorpay_bp.route("/refund", methods=["POST"])
@jwt_required()
def process_razorpay_refund():
    """
    Admin-only refund endpoint:
      - Validates Admin role.
      - Calls Razorpay API to issue full or partial refund.
      - Updates Payment, Billing, Order, and OrderStatusHistory records.
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or (user.role or "").lower() not in ("admin", "staff"):
        return jsonify({"message": "Admin privileges required to process refunds."}), 403

    data = request.get_json(silent=True) or {}
    payment_id_or_gw = data.get("payment_id")
    refund_amount = data.get("amount")  # Optional float
    reason = data.get("reason", "Customer requested cancellation / return")

    if not payment_id_or_gw:
        return jsonify({"message": "Payment ID is required"}), 400

    payment = None
    if str(payment_id_or_gw).isdigit():
        payment = Payment.query.get(int(payment_id_or_gw))
    if not payment:
        payment = Payment.query.filter_by(gateway_payment_id=str(payment_id_or_gw)).first()
    if not payment:
        payment = Payment.query.filter_by(transaction_id=str(payment_id_or_gw)).first()

    if not payment:
        return jsonify({"message": "Payment record not found"}), 404

    if not payment.gateway_payment_id:
        return jsonify({"message": "No gateway payment ID recorded for this payment."}), 400

    orig_amount = float(payment.amount)
    already_refunded = float(payment.refunded_amount or 0.0)
    max_refundable = round(orig_amount - already_refunded, 2)

    if max_refundable <= 0:
        return jsonify({"message": "Payment has already been fully refunded."}), 400

    amt_to_refund = None
    if refund_amount is not None:
        try:
            amt_to_refund = float(refund_amount)
        except (ValueError, TypeError):
            return jsonify({"message": "Invalid refund amount"}), 400

        if amt_to_refund <= 0 or amt_to_refund > max_refundable:
            return jsonify({
                "message": f"Refund amount must be between ₹1.00 and ₹{max_refundable:.2f}"
            }), 400

    try:
        notes = {
            "reason": reason,
            "admin_user": user.username,
            "order_id": str(payment.order_id or "")
        }
        rzp_refund = RazorpayService.create_refund(
            payment_id=payment.gateway_payment_id,
            amount_in_rupees=amt_to_refund,
            notes=notes
        )

        refund_id = rzp_refund.get("id")
        actual_refunded_paise = rzp_refund.get("amount", 0)
        actual_refunded_rupees = RazorpayService.paise_to_rupees(actual_refunded_paise)

        payment.refund_id = refund_id
        payment.refunded_amount = round(already_refunded + actual_refunded_rupees, 2)
        payment.refund_status = "full" if payment.refunded_amount >= orig_amount else "partial"
        payment.updated_at = datetime.utcnow()

        order = payment.order_rel or (payment.billing.order_rel if payment.billing else None)
        billing = payment.billing or (order.billing if order else None)

        if payment.refund_status == "full":
            if billing:
                billing.payment_status = "Refunded"
            if order:
                order.status = "Refunded"

        if order:
            history = OrderStatusHistory(
                order_id=order.id,
                status=order.status,
                notes=(
                    f"Refund of ₹{actual_refunded_rupees:.2f} issued via Razorpay ({refund_id}). "
                    f"Reason: {reason}. Admin: {user.username}"
                )
            )
            db.session.add(history)

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": f"Successfully refunded ₹{actual_refunded_rupees:.2f}",
            "refund_id": refund_id,
            "refund_status": payment.refund_status,
            "total_refunded": payment.refunded_amount,
            "remaining_amount": round(orig_amount - payment.refunded_amount, 2)
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.exception("Error processing refund: %s", str(e))
        return jsonify({"message": f"Refund failed: {str(e)}"}), 500


# ---------------------------------------------------------------------------
# 8. GET /transactions — Admin Transaction Analytics & List
# ---------------------------------------------------------------------------
@razorpay_bp.route("/transactions", methods=["GET"])
@jwt_required()
def get_razorpay_transactions():
    """
    Admin-only transaction list and summary metrics.
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or (user.role or "").lower() not in ("admin", "staff"):
        return jsonify({"message": "Admin privileges required."}), 403

    query = Payment.query.filter(Payment.gateway == "Razorpay")

    # Optional status filter
    status_filter = request.args.get("status")
    if status_filter:
        query = query.filter(Payment.gateway_status == status_filter)

    # Optional search by transaction ID or order ID
    search_q = request.args.get("search", "").strip()
    if search_q:
        query = query.filter(
            (Payment.gateway_payment_id.ilike(f"%{search_q}%")) |
            (Payment.gateway_order_id.ilike(f"%{search_q}%")) |
            (Payment.transaction_id.ilike(f"%{search_q}%"))
        )

    payments = query.order_by(Payment.id.desc()).all()

    # Calculate summary metrics
    total_volume = 0.0
    total_refunded = 0.0
    captured_count = 0
    failed_count = 0
    pending_count = 0

    results = []
    for p in payments:
        p_dict = p.to_dict()
        results.append(p_dict)

        if p.gateway_status == "captured" or p.signature_verified:
            total_volume += float(p.amount or 0.0)
            captured_count += 1
        elif p.gateway_status == "failed":
            failed_count += 1
        else:
            pending_count += 1

        total_refunded += float(p.refunded_amount or 0.0)

    return jsonify({
        "status": "success",
        "metrics": {
            "total_transactions": len(payments),
            "captured_count": captured_count,
            "failed_count": failed_count,
            "pending_count": pending_count,
            "total_volume": round(total_volume, 2),
            "total_refunded": round(total_refunded, 2),
            "net_revenue": round(total_volume - total_refunded, 2)
        },
        "transactions": results
    }), 200


# ---------------------------------------------------------------------------
# 9. GET & POST /admin/credentials — Admin Razorpay Account Management
# ---------------------------------------------------------------------------
@razorpay_bp.route("/admin/credentials", methods=["GET"])
@jwt_required()
def get_admin_razorpay_credentials():
    """
    Get current configured Razorpay account metadata (Key ID, Mode, Currency).
    Does not expose raw secret.
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or (user.role or "").lower() not in ("admin", "staff"):
        return jsonify({"message": "Admin privileges required."}), 403

    return jsonify({
        "status": "success",
        "configured": RazorpayService.is_configured(),
        "key_id": Config.RAZORPAY_KEY_ID or "",
        "mode": Config.RAZORPAY_MODE or "test",
        "currency": Config.RAZORPAY_CURRENCY or "INR",
        "has_secret": bool(Config.RAZORPAY_KEY_SECRET),
        "has_webhook_secret": bool(Config.RAZORPAY_WEBHOOK_SECRET)
    }), 200


@razorpay_bp.route("/admin/credentials", methods=["POST"])
@jwt_required()
def update_admin_razorpay_credentials():
    """
    Validate and save admin's Razorpay credentials (Key ID, Key Secret, Mode).
    Tests connection against Razorpay API before committing.
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or (user.role or "").lower() not in ("admin", "staff"):
        return jsonify({"message": "Admin privileges required."}), 403

    data = request.get_json(silent=True) or {}
    new_key_id = (data.get("key_id") or "").strip()
    new_key_secret = (data.get("key_secret") or "").strip()
    new_webhook_secret = (data.get("webhook_secret") or "").strip()
    new_mode = (data.get("mode") or "test").strip().lower()

    if not new_key_id:
        return jsonify({"message": "Razorpay Key ID is required."}), 400

    # If secret not passed, keep existing
    secret_to_use = new_key_secret or Config.RAZORPAY_KEY_SECRET
    if not secret_to_use:
        return jsonify({"message": "Razorpay Key Secret is required."}), 400

    # Test authentication directly with Razorpay
    import razorpay
    try:
        test_client = razorpay.Client(auth=(new_key_id, secret_to_use))
        test_client.order.all({"count": 1})
    except Exception as e:
        logger.warning("Razorpay credentials validation failed: %s", str(e))
        return jsonify({
            "status": "failed",
            "message": f"Razorpay authentication failed: {str(e)}. Please check your Key ID and Secret."
        }), 400

    # Update runtime config
    Config.RAZORPAY_KEY_ID = new_key_id
    Config.RAZORPAY_KEY_SECRET = secret_to_use
    if new_webhook_secret:
        Config.RAZORPAY_WEBHOOK_SECRET = new_webhook_secret
    Config.RAZORPAY_MODE = new_mode

    # Update .env file on disk
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    try:
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as ef:
                env_lines = ef.readlines()

            keys_to_set = {
                'RAZORPAY_KEY_ID': new_key_id,
                'RAZORPAY_KEY_SECRET': secret_to_use,
                'RAZORPAY_MODE': new_mode
            }
            if new_webhook_secret:
                keys_to_set['RAZORPAY_WEBHOOK_SECRET'] = new_webhook_secret

            new_lines = []
            found_keys = set()
            for line in env_lines:
                matched = False
                for k, v in keys_to_set.items():
                    if line.startswith(f"{k}="):
                        new_lines.append(f"{k}={v}\n")
                        found_keys.add(k)
                        matched = True
                        break
                if not matched:
                    new_lines.append(line)

            for k, v in keys_to_set.items():
                if k not in found_keys:
                    new_lines.append(f"{k}={v}\n")

            with open(env_path, 'w', encoding='utf-8') as ef:
                ef.writelines(new_lines)
    except Exception as env_err:
        logger.error("Failed to write updated credentials to .env: %s", str(env_err))

    return jsonify({
        "status": "success",
        "message": "Razorpay account credentials verified and updated successfully!",
        "key_id": new_key_id,
        "mode": new_mode,
        "configured": True
    }), 200
