from app import create_app
from models import db, User, Customer, CustomerProfile, Frame, Lens, Order, OrderItem, Appointment, EyeTest, Prescription, Billing, Brand, Category
from datetime import datetime, date
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    print("Creating all tables from normalized schema...")
    db.create_all()

    print("Generating sample data...")
    
    # 1. User
    admin = User(username='admin', password_hash=generate_password_hash('admin123'), email='admin@visionedge.com', role='admin')
    db.session.add(admin)
    db.session.commit()

    # 2. Customers
    print("Inserting 20 Customers...")
    customers = []
    for i in range(1, 21):
        c = Customer(
            customer_code=f'CUST{i:03d}',
            first_name=f'Test{i}',
            last_name='User',
            phone=f'987654321{i-1}',
            email=f'test{i}@example.com',
            age=30+i,
            city='Mumbai',
            created_by=admin.id
        )
        db.session.add(c)
        db.session.flush()
        customers.append(c)
        
        # Profile
        cp = CustomerProfile(
            customer_id=c.id,
            blood_group='O+',
            eye_conditions='Myopia' if i % 2 == 0 else 'None',
            notes=f'Notes for customer {i}'
        )
        db.session.add(cp)
    db.session.commit()

    # 3. Inventory (20 Frames, 20 Lenses)
    print("Inserting 50 Frames and 30 Lenses...")
    frames = []
    for i in range(1, 51):
        f = Frame(
            frame_code=f'FRM{i:03d}',
            brand='RayBan' if i % 2 == 0 else 'Oakley',
            model=f'Model-X{i}',
            name=f'Frame X{i}',
            shape='Square',
            color='Black',
            price=2500.0,
            stock=15,
            min_stock=5
        )
        db.session.add(f)
        frames.append(f)
        
    lenses = []
    for i in range(1, 31):
        l = Lens(
            lens_code=f'LNS{i:03d}',
            brand='Zeiss' if i % 2 == 0 else 'Essilor',
            type='Single Vision' if i % 2 == 0 else 'Progressive',
            coating='Anti Glare',
            price=1500.0,
            stock=20,
            min_stock=10
        )
        db.session.add(l)
        lenses.append(l)
    db.session.commit()

    # 4. 5 Appointments
    print("Inserting 20 Appointments...")
    for i in range(20):
        apt = Appointment(
            customer_id=customers[i % 20].id,
            appointment_date=date(2026, 8, (i%28)+1),
            appointment_time=datetime.strptime('10:00:00', '%H:%M:%S').time(),
            appointment_type='Eye Test',
            doctor_name='Dr. Smith',
            status='Pending'
        )
        db.session.add(apt)
    db.session.commit()

    # 5. 10 Prescriptions (and Eye Tests)
    print("Inserting 20 EyeTests and Prescriptions...")
    prescriptions = []
    for i in range(20):
        # Eye test
        et = EyeTest(
            customer_id=customers[i % 20].id,
            right_sphere='-1.00', right_cylinder='-0.50', right_axis='180',
            left_sphere='-1.25', left_cylinder='-0.50', left_axis='175',
            pd_value='62', remarks='Standard myopia'
        )
        db.session.add(et)
        db.session.flush()
        
        # Prescription
        pr = Prescription(
            prescription_number=f'RX{i:03d}',
            customer_id=customers[i % 20].id,
            eye_test_id=et.id,
            add_power='',
            doctor_name='Dr. Smith',
            status='Completed'
        )
        db.session.add(pr)
        prescriptions.append(pr)
    db.session.commit()

    # 6. 10 Orders
    print("Inserting 30 Orders...")
    for i in range(30):
        o = Order(
            order_id=f'ORD{i:03d}',
            order_number=f'ORD{i:03d}',
            customer_id=customers[i % 20].id,
            prescription_id=prescriptions[i % 20].id,
            status='Pending',
            total_amount=4000.0
        )
        db.session.add(o)
        db.session.flush()
        
        # Items
        f_idx = i % 50
        l_idx = i % 30
        oi1 = OrderItem(order_id=o.id, product_type='Frame', product_id=frames[f_idx].id, price=2500.0)
        oi2 = OrderItem(order_id=o.id, product_type='Lens', product_id=lenses[l_idx].id, price=1500.0)
        db.session.add(oi1)
        db.session.add(oi2)
        
        # Billing
        b = Billing(
            invoice_number=f'INV{i:03d}',
            order_id=o.id,
            subtotal=4000.0,
            total_amount=4000.0,
            payment_status='Pending',
            payment_method='Cash'
        )
        db.session.add(b)
    db.session.commit()

    print("=========================================")
    print("Successfully migrated completely to MySQL!")
    print("Created all tables and inserted requested sample data.")
