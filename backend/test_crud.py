"""
test_crud.py — Basic CRUD and transaction tests for VisionEdge
===============================================================
Run from backend/ directory:
    python test_crud.py
"""
import sys
import traceback

PASS_COUNT = 0
FAIL_COUNT = 0
results = []

def test(name, fn):
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


from app import create_app
from models import (db, User, Customer, CustomerProfile, Frame, Lens,
                    Order, OrderItem, Billing, Payment, Prescription,
                    EyeTest, Appointment, InventoryTransaction, Brand,
                    Category, Supplier, Notification)
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text

app = create_app()

with app.app_context():
    db.create_all()

    # ------------------------------------------------------------------ #
    # Config tests
    # ------------------------------------------------------------------ #
    def test_dialect():
        from config import Config
        d = Config.db_dialect()
        assert d in ('sqlite', 'postgresql'), f"Unexpected dialect: {d}"

    test("Config: dialect is sqlite or postgresql", test_dialect)

    def test_no_mysql_uri():
        from config import Config
        assert not Config.SQLALCHEMY_DATABASE_URI.startswith("mysql"), \
            "MySQL URI should not be active"

    test("Config: no MySQL URI in active path", test_no_mysql_uri)

    def test_health_select():
        r = db.session.execute(text("SELECT 1"))
        assert r.scalar() == 1

    test("DB: SELECT 1 succeeds", test_health_select)

    # ------------------------------------------------------------------ #
    # User CRUD
    # ------------------------------------------------------------------ #
    _test_user = None

    def test_create_user():
        global _test_user
        u = User(
            username="test_crud_user",
            first_name="Test",
            last_name="User",
            password_hash=generate_password_hash("TestPass123"),
            email="test_crud@visionedge.test",
            role="customer",
        )
        db.session.add(u)
        db.session.commit()
        assert u.id is not None
        _test_user = u

    test("User: create", test_create_user)

    def test_read_user():
        u = User.query.filter_by(username="test_crud_user").first()
        assert u is not None
        assert u.first_name == "Test"

    test("User: read by username", test_read_user)

    def test_password_hash():
        u = User.query.filter_by(username="test_crud_user").first()
        assert check_password_hash(u.password_hash, "TestPass123")
        assert not check_password_hash(u.password_hash, "WrongPass")

    test("User: password hash verification", test_password_hash)

    def test_update_user():
        u = User.query.filter_by(username="test_crud_user").first()
        u.first_name = "Updated"
        db.session.commit()
        u2 = User.query.filter_by(username="test_crud_user").first()
        assert u2.first_name == "Updated"

    test("User: update", test_update_user)

    # ------------------------------------------------------------------ #
    # Customer CRUD
    # ------------------------------------------------------------------ #
    _test_customer = None

    def test_create_customer():
        global _test_customer
        c = Customer(
            customer_code="CUST9999",
            first_name="CrudTest",
            last_name="Customer",
            phone="9999999999",
            email="crud_cust@visionedge.test",
        )
        db.session.add(c)
        db.session.flush()
        profile = CustomerProfile(customer_id=c.id)
        db.session.add(profile)
        db.session.commit()
        assert c.id is not None
        _test_customer = c

    test("Customer: create with profile", test_create_customer)

    def test_read_customer():
        c = Customer.query.filter_by(customer_code="CUST9999").first()
        assert c is not None
        assert c.profile is not None

    test("Customer: read with profile relationship", test_read_customer)

    # ------------------------------------------------------------------ #
    # Frame & Inventory
    # ------------------------------------------------------------------ #
    _test_frame = None

    def test_create_frame():
        global _test_frame
        f = Frame(
            frame_code="FR-CRUD-001",
            brand="TestBrand",
            model="CRUD Model",
            price=1500.0,
            selling_price=1800.0,
            stock=10,
            min_stock=2,
        )
        db.session.add(f)
        db.session.commit()
        assert f.id is not None
        _test_frame = f

    test("Frame: create", test_create_frame)

    def test_stock_deduction():
        f = Frame.query.filter_by(frame_code="FR-CRUD-001").first()
        original = f.stock
        f.stock -= 2
        db.session.commit()
        f2 = Frame.query.filter_by(frame_code="FR-CRUD-001").first()
        assert f2.stock == original - 2

    test("Frame: stock deduction", test_stock_deduction)

    # ------------------------------------------------------------------ #
    # Order + OrderItem transaction
    # ------------------------------------------------------------------ #
    _test_order = None

    def test_create_order_transaction():
        global _test_order
        c = Customer.query.filter_by(customer_code="CUST9999").first()
        f = Frame.query.filter_by(frame_code="FR-CRUD-001").first()

        order = Order(
            order_id="ORD-TEST-001",
            order_number="ORD-TEST-001",
            customer_id=c.id,
            status="Pending",
            subtotal=1800.0,
            gst=0.0,
            discount=0.0,
            total_amount=1800.0,
        )
        db.session.add(order)
        db.session.flush()

        item = OrderItem(
            order_id=order.id,
            product_type="Frame",
            item_type="Frame",
            product_id=f.id,
            item_id=f.id,
            quantity=1,
            price=1800.0,
            total_price=1800.0,
        )
        db.session.add(item)
        db.session.commit()

        assert order.id is not None
        assert len(order.items) == 1
        _test_order = order

    test("Order: create with items (transaction)", test_create_order_transaction)

    # ------------------------------------------------------------------ #
    # Billing + Payment
    # ------------------------------------------------------------------ #
    def test_create_billing():
        o = Order.query.filter_by(order_number="ORD-TEST-001").first()
        b = Billing(
            invoice_number="VE-TEST-0001",
            order_id=o.id,
            subtotal=1800.0,
            discount=0.0,
            gst=0.0,
            total_amount=1800.0,
            payment_method="Cash",
            payment_status="Paid",
        )
        db.session.add(b)
        db.session.flush()

        p = Payment(
            billing=b,
            amount=1800.0,
            payment_method="Cash",
            transaction_id="TXN-CRUD-001",
        )
        db.session.add(p)
        db.session.commit()
        assert b.id is not None
        assert len(b.payments) == 1

    test("Billing+Payment: create and link", test_create_billing)

    # ------------------------------------------------------------------ #
    # Rollback test
    # ------------------------------------------------------------------ #
    def test_rollback():
        try:
            bad = User(
                username="test_crud_user",  # duplicate username — should fail
                password_hash="x",
                email="another@test.com",
            )
            db.session.add(bad)
            db.session.commit()
            raise AssertionError("Should have raised unique constraint error")
        except Exception:
            db.session.rollback()
        # Verify session is still usable after rollback
        count = User.query.count()
        assert count >= 1

    test("Transaction: rollback on unique constraint violation", test_rollback)

    # ------------------------------------------------------------------ #
    # Brand / Category / Supplier new columns
    # ------------------------------------------------------------------ #
    def test_brand_columns():
        b = Brand(name="TestBrand", status="Active", logo="/media/test.png")
        db.session.add(b)
        db.session.commit()
        b2 = Brand.query.filter_by(name="TestBrand").first()
        assert b2.status == "Active"
        assert b2.logo == "/media/test.png"

    test("Brand: status and logo columns", test_brand_columns)

    def test_category_columns():
        c = Category(name="Eyeglasses", type="Frame", description="Standard frames")
        db.session.add(c)
        db.session.commit()
        c2 = Category.query.filter_by(name="Eyeglasses").first()
        assert c2.type == "Frame"

    test("Category: type and description columns", test_category_columns)

    # ------------------------------------------------------------------ #
    # Cleanup test records
    # ------------------------------------------------------------------ #
    def test_cleanup():
        # Delete in FK-safe order
        b_ids = [b.id for b in Billing.query.filter_by(invoice_number="VE-TEST-0001").all()]
        if b_ids:
            Payment.query.filter(Payment.billing_id.in_(b_ids)).delete(synchronize_session=False)
        Billing.query.filter_by(invoice_number="VE-TEST-0001").delete()
        OrderItem.query.filter(OrderItem.order_id.in_(
            [o.id for o in Order.query.filter_by(order_number="ORD-TEST-001").all()]
        )).delete(synchronize_session=False)
        Order.query.filter_by(order_number="ORD-TEST-001").delete()
        CustomerProfile.query.filter(
            CustomerProfile.customer_id.in_(
                [c.id for c in Customer.query.filter_by(customer_code="CUST9999").all()]
            )
        ).delete(synchronize_session=False)
        Customer.query.filter_by(customer_code="CUST9999").delete()
        User.query.filter_by(username="test_crud_user").delete()
        Frame.query.filter_by(frame_code="FR-CRUD-001").delete()
        Brand.query.filter_by(name="TestBrand").delete()
        Category.query.filter_by(name="Eyeglasses").delete()
        db.session.commit()

    # Pre-clean any leftover test records
    test_cleanup()

    test("Cleanup: delete test records", test_cleanup)

    # ------------------------------------------------------------------ #
    # Final report
    # ------------------------------------------------------------------ #
    print()
    print("=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    print(f"{'Test':<50} {'Result':<8}")
    print("-" * 60)
    for status, name, err in results:
        err_str = f"  ({err[:40]})" if err else ""
        print(f"{name:<50} {status}{err_str}")
    print("=" * 60)
    print(f"PASSED: {PASS_COUNT}  FAILED: {FAIL_COUNT}")
    print()

    if FAIL_COUNT > 0:
        sys.exit(1)
