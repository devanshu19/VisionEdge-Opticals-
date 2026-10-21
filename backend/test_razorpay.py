"""
test_razorpay.py — VisionEdge Razorpay Payment Gateway Integration Test Suite
=============================================================================
Tests:
  1. Service Config & Readiness
  2. Currency & Paise Transformations
  3. HMAC Signature Verification & Tamper Detection
  4. Webhook Signature Verification
  5. Public Config Endpoint (/api/payment/razorpay/config)
  6. Secure Authoritative Order Creation (/api/payment/razorpay/create-order)
  7. Payment Verification & Idempotency (/api/payment/razorpay/verify)
  8. Webhook Processing & Deduplication (/api/payment/razorpay/webhook)
  9. Order Payment Status Query (/api/payment/razorpay/status/<id>)
 10. Payment Retry Initiation (/api/payment/razorpay/retry)
 11. Admin Refund Processing (/api/payment/razorpay/refund)
 12. Direct Checkout Security Bypass Prevention

Run from backend directory:
    python test_razorpay.py
"""

import sys
import os
import json
import hmac
import hashlib
from datetime import datetime
from unittest.mock import patch, MagicMock

# Ensure backend directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from config import Config
from models import (
    db, User, Customer, Frame, Lens, Order, OrderItem,
    Billing, Payment, WebhookEvent, OrderStatusHistory
)
from services.razorpay_service import RazorpayService
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token

PASS_COUNT = 0
FAIL_COUNT = 0
results = []


def run_test(name, fn):
    global PASS_COUNT, FAIL_COUNT
    try:
        fn()
        results.append(("PASS", name, ""))
        PASS_COUNT += 1
        print(f"  PASS  {name}")
    except Exception as e:
        results.append(("FAIL", name, str(e)))
        FAIL_COUNT += 1
        print(f"  FAIL  {name}: {e}")


app = create_app()
app.config["TESTING"] = True

with app.app_context():
    # Setup test database tables
    db.create_all()

    # Create test fixtures
    # 1. Admin user
    admin_user = User.query.filter_by(username="test_admin_rzp").first()
    if not admin_user:
        admin_user = User(
            username="test_admin_rzp",
            email="admin_rzp@visionedge.com",
            password_hash=generate_password_hash("AdminPass123!"),
            role="admin",
            first_name="Admin",
            last_name="Tester"
        )
        db.session.add(admin_user)

    # 2. Regular customer user
    customer_user = User.query.filter_by(username="test_cust_rzp").first()
    if not customer_user:
        customer_user = User(
            username="test_cust_rzp",
            email="cust_rzp@visionedge.com",
            password_hash=generate_password_hash("CustPass123!"),
            role="customer",
            first_name="Rahul",
            last_name="Sharma",
            phone="9876543210",
            address="123 MG Road, Bengaluru"
        )
        db.session.add(customer_user)
        db.session.flush()

    # Customer profile
    cust_profile = Customer.query.filter_by(created_by=customer_user.id).first()
    if not cust_profile:
        cust_profile = Customer(
            customer_code="CUST-RZP-01",
            first_name="Rahul",
            last_name="Sharma",
            phone="9876543210",
            email="cust_rzp@visionedge.com",
            address="123 MG Road, Bengaluru",
            created_by=customer_user.id
        )
        db.session.add(cust_profile)

    # 3. Another user (for authorization boundary test)
    other_user = User.query.filter_by(username="test_other_rzp").first()
    if not other_user:
        other_user = User(
            username="test_other_rzp",
            email="other_rzp@visionedge.com",
            password_hash=generate_password_hash("OtherPass123!"),
            role="customer",
            first_name="Pooja",
            last_name="Patel"
        )
        db.session.add(other_user)

    # 4. Test Frame
    test_frame = Frame.query.filter_by(model="RZP-TITAN-01").first()
    if not test_frame:
        test_frame = Frame(
            name="Razor Titanium Frame",
            frame_code="FRM-RZP-01",
            brand="Ray-Ban",
            model="RZP-TITAN-01",
            price=2000.0,
            selling_price=2000.0,
            stock=50,
            min_stock=5,
            shape="Rectangle",
            status="Active"
        )
        db.session.add(test_frame)

    db.session.commit()

    admin_id = admin_user.id
    customer_id = customer_user.id
    other_id = other_user.id
    frame_id = test_frame.id

    admin_token = create_access_token(identity=str(admin_id))
    customer_token = create_access_token(identity=str(customer_id))
    other_token = create_access_token(identity=str(other_id))

client = app.test_client()

print("\n" + "=" * 60)
print("RUNNING VISIONEDGE RAZORPAY TEST SUITE")
print("=" * 60)


# ---------------------------------------------------------------------------
# Test 1: Service Config & Keys
# ---------------------------------------------------------------------------
def test_service_config():
    assert RazorpayService.is_configured() is True, "Razorpay should be configured"
    client_instance = RazorpayService.get_client()
    assert client_instance is not None, "Razorpay client should initialize"


run_test("RazorpayService: configuration & client initialization", test_service_config)


# ---------------------------------------------------------------------------
# Test 2: Paise Transformation & Rounding
# ---------------------------------------------------------------------------
def test_paise_conversion():
    assert RazorpayService.rupees_to_paise(1.0) == 100
    assert RazorpayService.rupees_to_paise(1499.50) == 149950
    assert RazorpayService.rupees_to_paise(2499.99) == 249999
    assert RazorpayService.paise_to_rupees(149950) == 1499.50
    assert RazorpayService.paise_to_rupees(100) == 1.00


run_test("RazorpayService: rupee <-> paise transformations", test_paise_conversion)


# ---------------------------------------------------------------------------
# Test 3: Signature Verification & Tamper Detection
# ---------------------------------------------------------------------------
def test_signature_verification():
    order_id = "order_test_12345"
    payment_id = "pay_test_67890"
    secret = Config.RAZORPAY_KEY_SECRET

    # Generate legitimate HMAC
    msg = f"{order_id}|{payment_id}".encode("utf-8")
    valid_sig = hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()

    # Valid check
    is_valid, err = RazorpayService.verify_payment_signature(order_id, payment_id, valid_sig)
    assert is_valid is True, f"Expected valid signature, got error: {err}"

    # Tampered signature check
    tampered_sig = valid_sig[:-4] + "ffff"
    is_invalid, err = RazorpayService.verify_payment_signature(order_id, payment_id, tampered_sig)
    assert is_invalid is False, "Tampered signature should fail verification"

    # Missing params check
    is_empty, _ = RazorpayService.verify_payment_signature("", payment_id, valid_sig)
    assert is_empty is False, "Empty order_id should fail verification"


run_test("RazorpayService: HMAC signature verification & tamper detection", test_signature_verification)


# ---------------------------------------------------------------------------
# Test 4: Webhook Signature Verification
# ---------------------------------------------------------------------------
def test_webhook_signature():
    payload_bytes = b'{"event":"payment.captured","id":"evt_123"}'
    webhook_secret = Config.RAZORPAY_WEBHOOK_SECRET
    valid_sig = hmac.new(webhook_secret.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()

    is_valid, err = RazorpayService.verify_webhook_signature(payload_bytes, valid_sig)
    assert is_valid is True, f"Expected valid webhook signature, got {err}"

    # Invalid signature
    is_invalid, _ = RazorpayService.verify_webhook_signature(payload_bytes, "invalid_sig_hex")
    assert is_invalid is False, "Invalid webhook signature should be rejected"


run_test("RazorpayService: Webhook signature verification", test_webhook_signature)


# ---------------------------------------------------------------------------
# Test 5: Public Config Endpoint
# ---------------------------------------------------------------------------
def test_public_config_endpoint():
    res = client.get("/api/payment/razorpay/config")
    assert res.status_code == 200
    data = res.get_json()
    assert data["configured"] is True
    assert data["key_id"] == Config.RAZORPAY_KEY_ID
    assert data["currency"] == "INR"
    assert "key_secret" not in data, "Never leak secret key in config endpoint!"
    assert "webhook_secret" not in data, "Never leak webhook secret!"


run_test("GET /api/payment/razorpay/config: returns public key only", test_public_config_endpoint)


# ---------------------------------------------------------------------------
# Test 6: Authoritative Order Creation Endpoint
# ---------------------------------------------------------------------------
global_test_order_info = {}


def test_create_order_endpoint():
    global global_test_order_info

    # 1. Unauthenticated request should be rejected
    unauth_res = client.post("/api/payment/razorpay/create-order", json={"items": []})
    assert unauth_res.status_code == 401, "Unauthenticated request must return 401"

    # 2. Authenticated request with coupon VISION30 (30% discount)
    # Frame price: 2000. Qty: 1.
    # Subtotal: 2000. GST (18%): 360. Discount (30% of 2000): 600.
    # Expected final amount: 2000 + 360 - 600 = 1760.00
    # Expected paise: 176000
    payload = {
        "shipping_address": "123 MG Road, Bengaluru",
        "phone": "9876543210",
        "coupon_code": "VISION30",
        "items": [
            {
                "item_type": "Frame",
                "item_id": frame_id,
                "quantity": 1
            }
        ]
    }

    # Mock Razorpay API order create to avoid external network dependency in unit test
    mock_rzp_order = {
        "id": "order_mock_test_778899",
        "amount": 176000,
        "currency": "INR",
        "receipt": "ORD-TEST-001",
        "status": "created"
    }

    with patch.object(RazorpayService, "create_order", return_value=mock_rzp_order):
        res = client.post(
            "/api/payment/razorpay/create-order",
            headers={"Authorization": f"Bearer {customer_token}"},
            json=payload
        )
        assert res.status_code == 201, f"Expected 201, got {res.status_code}: {res.get_data(as_text=True)}"
        data = res.get_json()
        assert data["status"] == "success"
        assert data["razorpay_order_id"] == "order_mock_test_778899"
        assert data["subtotal"] == 2000.0
        assert data["gst"] == 360.0
        assert data["discount"] == 600.0
        assert data["total_amount"] == 1760.0
        assert data["key_id"] == Config.RAZORPAY_KEY_ID

        global_test_order_info = {
            "order_id": data["order_id"],
            "order_number": data["order_number"],
            "razorpay_order_id": data["razorpay_order_id"],
            "amount": data["total_amount"]
        }


run_test("POST /api/payment/razorpay/create-order: authoritative price & order creation", test_create_order_endpoint)


# ---------------------------------------------------------------------------
# Test 7: Payment Verification Endpoint & Idempotency
# ---------------------------------------------------------------------------
def test_verify_payment_endpoint():
    rzp_order_id = global_test_order_info["razorpay_order_id"]
    rzp_payment_id = "pay_mock_success_112233"
    secret = Config.RAZORPAY_KEY_SECRET

    msg = f"{rzp_order_id}|{rzp_payment_id}".encode("utf-8")
    valid_sig = hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()

    # 1. Invalid signature test
    bad_payload = {
        "razorpay_order_id": rzp_order_id,
        "razorpay_payment_id": rzp_payment_id,
        "razorpay_signature": "bad_sig_here"
    }
    bad_res = client.post(
        "/api/payment/razorpay/verify",
        headers={"Authorization": f"Bearer {customer_token}"},
        json=bad_payload
    )
    assert bad_res.status_code == 400, "Bad signature must return 400"

    # 2. Valid signature & gateway fetch mock
    mock_payment_fetch = {
        "id": rzp_payment_id,
        "order_id": rzp_order_id,
        "amount": 176000,
        "currency": "INR",
        "status": "captured",
        "method": "card"
    }

    with patch.object(RazorpayService, "fetch_payment", return_value=mock_payment_fetch):
        verify_payload = {
            "razorpay_order_id": rzp_order_id,
            "razorpay_payment_id": rzp_payment_id,
            "razorpay_signature": valid_sig,
            "order_id": global_test_order_info["order_id"]
        }
        res = client.post(
            "/api/payment/razorpay/verify",
            headers={"Authorization": f"Bearer {customer_token}"},
            json=verify_payload
        )
        assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.get_data(as_text=True)}"
        data = res.get_json()
        assert data["status"] == "success"
        assert data["payment_status"] == "Paid"

        # Check database records
        with app.app_context():
            ord_rec = Order.query.get(global_test_order_info["order_id"])
            assert ord_rec.status == "Confirmed", f"Order status should be Confirmed, got {ord_rec.status}"
            assert ord_rec.billing.payment_status == "Paid"

            pay_rec = Payment.query.filter_by(gateway_order_id=rzp_order_id).first()
            assert pay_rec.signature_verified is True
            assert pay_rec.gateway_status == "captured"
            assert pay_rec.gateway_payment_id == rzp_payment_id

        # 3. Idempotency test: Re-verification must succeed gracefully without duplicating
        res_repeat = client.post(
            "/api/payment/razorpay/verify",
            headers={"Authorization": f"Bearer {customer_token}"},
            json=verify_payload
        )
        assert res_repeat.status_code == 200, "Repeat verification should return 200 (idempotent)"
        assert res_repeat.get_json()["message"] == "Payment has already been verified."


run_test("POST /api/payment/razorpay/verify: signature verification & idempotency", test_verify_payment_endpoint)


# ---------------------------------------------------------------------------
# Test 8: Webhook Endpoint & Deduplication
# ---------------------------------------------------------------------------
def test_webhook_processing():
    event_id = "evt_test_webhook_9988"
    webhook_body = json.dumps({
        "entity": "event",
        "account_id": "acc_test",
        "event": "payment.captured",
        "id": event_id,
        "payload": {
            "payment": {
                "entity": {
                    "id": "pay_mock_webhook_4455",
                    "order_id": global_test_order_info["razorpay_order_id"],
                    "amount": 176000,
                    "currency": "INR",
                    "status": "captured"
                }
            }
        }
    }).encode("utf-8")

    secret = Config.RAZORPAY_WEBHOOK_SECRET
    sig = hmac.new(secret.encode("utf-8"), webhook_body, hashlib.sha256).hexdigest()

    # 1. Invalid signature webhook
    bad_res = client.post(
        "/api/payment/razorpay/webhook",
        headers={"X-Razorpay-Signature": "invalid_sig"},
        data=webhook_body
    )
    assert bad_res.status_code == 400, "Invalid webhook signature must return 400"

    # 2. Valid signature webhook
    res = client.post(
        "/api/payment/razorpay/webhook",
        headers={"X-Razorpay-Signature": sig},
        data=webhook_body
    )
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"

    # Verify event stored in DB
    with app.app_context():
        ev = WebhookEvent.query.filter_by(event_id=event_id).first()
        assert ev is not None, "Webhook event must be recorded"
        assert ev.status == "processed"

    # 3. Deduplication: Repeat delivery should return 200 with already_processed
    res_dup = client.post(
        "/api/payment/razorpay/webhook",
        headers={"X-Razorpay-Signature": sig},
        data=webhook_body
    )
    assert res_dup.status_code == 200
    assert res_dup.get_json().get("status") == "already_processed"


run_test("POST /api/payment/razorpay/webhook: HMAC verification & event deduplication", test_webhook_processing)


# ---------------------------------------------------------------------------
# Test 9: Authoritative Status Endpoint
# ---------------------------------------------------------------------------
def test_status_endpoint():
    order_id = global_test_order_info["order_id"]

    # 1. Customer who owns the order can view status
    res = client.get(
        f"/api/payment/razorpay/status/{order_id}",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["order_id"] == order_id
    assert data["order_status"] == "Confirmed"
    assert data["payment"]["is_paid"] is True

    # 2. Other customer cannot view someone else's order (403)
    res_other = client.get(
        f"/api/payment/razorpay/status/{order_id}",
        headers={"Authorization": f"Bearer {other_token}"}
    )
    assert res_other.status_code == 403, "Access to other customer's order must be denied"

    # 3. Admin can view any order
    res_admin = client.get(
        f"/api/payment/razorpay/status/{order_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res_admin.status_code == 200


run_test("GET /api/payment/razorpay/status/<id>: authoritative status & auth check", test_status_endpoint)


# ---------------------------------------------------------------------------
# Test 10: Payment Retry Endpoint
# ---------------------------------------------------------------------------
def test_retry_endpoint():
    import uuid
    # Create a pending order for retry test
    with app.app_context():
        ord_num = f"ORD-RETRY-{uuid.uuid4().hex[:6].upper()}"
        cust = Customer.query.filter_by(created_by=customer_id).first()
        retry_ord = Order(
            order_id=ord_num,
            order_number=ord_num,
            customer_id=cust.id if cust else 1,
            status="Pending",
            total_amount=1200.0,
            subtotal=1200.0
        )
        db.session.add(retry_ord)
        db.session.commit()
        pending_order_id = retry_ord.id

    mock_retry_rzp = {
        "id": "order_mock_retry_9900",
        "amount": 120000,
        "currency": "INR",
        "receipt": "RETRY-ORD-RETRY-001",
        "status": "created"
    }

    with patch.object(RazorpayService, "create_order", return_value=mock_retry_rzp):
        res = client.post(
            "/api/payment/razorpay/retry",
            headers={"Authorization": f"Bearer {customer_token}"},
            json={"order_id": pending_order_id}
        )
        assert res.status_code == 200
        data = res.get_json()
        assert data["status"] == "success"
        assert data["razorpay_order_id"] == "order_mock_retry_9900"


run_test("POST /api/payment/razorpay/retry: generate fresh payment session", test_retry_endpoint)


# ---------------------------------------------------------------------------
# Test 11: Admin Refund Processing
# ---------------------------------------------------------------------------
def test_admin_refund():
    # 1. Non-admin must be forbidden (403)
    res_nonadmin = client.post(
        "/api/payment/razorpay/refund",
        headers={"Authorization": f"Bearer {customer_token}"},
        json={"payment_id": "pay_mock_success_112233"}
    )
    assert res_nonadmin.status_code == 403, "Non-admin refund must return 403"

    # 2. Admin partial refund
    mock_refund_resp = {
        "id": "rfn_mock_refund_12345",
        "payment_id": "pay_mock_success_112233",
        "amount": 50000,  # ₹500 in paise
        "status": "processed"
    }

    with patch.object(RazorpayService, "create_refund", return_value=mock_refund_resp):
        res = client.post(
            "/api/payment/razorpay/refund",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "payment_id": "pay_mock_success_112233",
                "amount": 500.0,
                "reason": "Customer requested partial refund"
            }
        )
        assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.get_data(as_text=True)}"
        data = res.get_json()
        assert data["status"] == "success"
        assert data["refund_id"] == "rfn_mock_refund_12345"
        assert data["refund_status"] == "partial"
        assert data["total_refunded"] == 500.0

    # 3. Verify Admin Transactions endpoint
    txns_res = client.get(
        "/api/payment/razorpay/transactions",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert txns_res.status_code == 200
    txns_data = txns_res.get_json()
    assert txns_data["status"] == "success"
    assert "metrics" in txns_data
    assert txns_data["metrics"]["total_transactions"] >= 1


run_test("POST /api/payment/razorpay/refund & GET transactions: admin refund flow", test_admin_refund)


# ---------------------------------------------------------------------------
# Test 12: Direct Checkout Security Bypass Prevention
# ---------------------------------------------------------------------------
def test_direct_checkout_security():
    # Trying to claim a Credit Card / Razorpay order via direct checkout must be rejected
    payload = {
        "payment_method": "Credit Card",
        "items": [{"item_type": "Frame", "item_id": frame_id, "quantity": 1}]
    }
    res = client.post(
        "/api/orders/checkout",
        headers={"Authorization": f"Bearer {customer_token}"},
        json=payload
    )
    assert res.status_code == 400, "Unverified online checkout claims must be rejected"

    # Cash on delivery should still be permitted
    cod_payload = {
        "payment_method": "Cash on Delivery",
        "items": [{"item_type": "Frame", "item_id": frame_id, "quantity": 1}]
    }
    cod_res = client.post(
        "/api/orders/checkout",
        headers={"Authorization": f"Bearer {customer_token}"},
        json=cod_payload
    )
    assert cod_res.status_code == 201
    cod_data = cod_res.get_json()
    assert cod_data["payment_status"] == "Pending", "COD payment status must be Pending"


run_test("Security: Direct checkout rejects fake online payment claims", test_direct_checkout_security)


# ---------------------------------------------------------------------------
# Summary Report
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("RAZORPAY TEST SUITE SUMMARY")
print("=" * 60)
for status, name, err in results:
    err_str = f" ({err})" if err else ""
    print(f"{status:5}  {name}{err_str}")
print("=" * 60)
print(f"TOTAL: {PASS_COUNT + FAIL_COUNT}  |  PASSED: {PASS_COUNT}  |  FAILED: {FAIL_COUNT}")
print("=" * 60 + "\n")

if FAIL_COUNT > 0:
    sys.exit(1)
else:
    sys.exit(0)
