from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ==========================================
# 1. User
# ==========================================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Login username
    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    # Customer's real first name
    first_name = db.Column(
        db.String(50),
        nullable=True
    )

    # Customer's real last name
    last_name = db.Column(
        db.String(50),
        nullable=True
    )

    # Password
    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    # Email
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=True
    )

    # Phone
    phone = db.Column(
        db.String(20)
    )

    # Customer details
    gender = db.Column(
        db.String(20)
    )

    date_of_birth = db.Column(
        db.Date
    )

    address = db.Column(
        db.Text
    )

    # User role
    role = db.Column(
        db.String(50),
        default='customer'
    )

    # Account creation date
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    def to_dict(self):

        # Create full name
        full_name = ""

        if self.first_name:
            full_name += self.first_name

        if self.last_name:
            if full_name:
                full_name += " "

            full_name += self.last_name


        # Fallback to username
        if not full_name:
            full_name = self.username


        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "name": full_name,
            "full_name": full_name,
            "email": self.email,
            "phone": self.phone,
            "gender": self.gender,
            "date_of_birth": str(self.date_of_birth) if self.date_of_birth else None,
            "address": self.address,
            "role": self.role
        }


# ==========================================
# 2. Customer
# ==========================================
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_code = db.Column(db.String(20), unique=True) # Keeping for compatibility
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    age = db.Column(db.Integer)
    phone = db.Column(db.String(20), nullable=False, index=True)
    alternate_phone = db.Column(db.String(20)) # Keeping for compatibility
    email = db.Column(db.String(120), index=True)
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100)) # Keeping for compatibility
    pincode = db.Column(db.String(20))
    occupation = db.Column(db.String(100))
    photo = db.Column(db.String(255))
    
    status = db.Column(db.String(20), default='Active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    profile = db.relationship('CustomerProfile', backref='customer', uselist=False, cascade="all, delete-orphan")
    prescriptions = db.relationship('Prescription', backref='customer', lazy=True, cascade="all, delete-orphan")
    appointments = db.relationship('Appointment', backref='customer_rel', lazy=True, cascade="all, delete-orphan")
    orders = db.relationship('Order', backref='customer', lazy=True)

    def to_dict(self):
        computed_age = self.age
        if self.date_of_birth and not computed_age:
            today = datetime.utcnow().date()
            computed_age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            
        return {
            "id": self.id, "customer_code": self.customer_code,
            "first_name": self.first_name, "last_name": self.last_name,
            "name": f"{self.first_name} {self.last_name}",
            "phone": self.phone, "alternate_phone": self.alternate_phone,
            "email": self.email, "gender": self.gender, 
            "dob": str(self.date_of_birth) if self.date_of_birth else None, "age": computed_age,
            "occupation": self.occupation,
            "address": self.address, "city": self.city, "state": self.state, "pincode": self.pincode,
            # Flatten profile fields for frontend compatibility
            "blood_group": self.profile.blood_group if self.profile else None,
            "eye_condition": self.profile.eye_conditions if self.profile else None,
            "allergies": self.profile.allergies if self.profile else None,
            "photo": self.photo,
            "status": self.status,
            "created_at": str(self.created_at)
        }

# ==========================================
# 3. Customer Profile
# ==========================================
class CustomerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, unique=True)
    blood_group = db.Column(db.String(10))
    eye_conditions = db.Column(db.Text)
    allergies = db.Column(db.Text)
    notes = db.Column(db.Text)

# ==========================================
# 4. Appointment
# ==========================================
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    appointment_type = db.Column(db.String(50)) # Eye Test, Frame Trial, Lens Consultation, Follow Up
    doctor_name = db.Column(db.String(100))
    status = db.Column(db.String(50), default='Pending') # Pending, Confirmed, Completed, Cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # We also keep a standard 'date' field to not break the frontend which expects a datetime for date
    # But wait, frontend expects date. I will combine appointment_date and appointment_time into a property or output.
    
    def to_dict(self):
        # Frontend expects 'date' combined string usually
        dt_str = f"{self.appointment_date} {self.appointment_time}" if self.appointment_date and self.appointment_time else None
        
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "customer_name": f"{self.customer_rel.first_name} {self.customer_rel.last_name}" if self.customer_rel else "Unknown",
            "doctor_name": self.doctor_name,
            "appointment_date": str(self.appointment_date),
            "appointment_time": str(self.appointment_time),
            "date": dt_str, # Compatibility
            "appointment_type": self.appointment_type,
            "status": self.status,
            "notes": self.notes,
            "created_at": str(self.created_at)
        }

# ==========================================
# 5. Eye Test
# ==========================================
class EyeTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=True)
    
    right_sphere = db.Column(db.String(20))
    right_cylinder = db.Column(db.String(20))
    right_axis = db.Column(db.String(20))
    
    left_sphere = db.Column(db.String(20))
    left_cylinder = db.Column(db.String(20))
    left_axis = db.Column(db.String(20))
    
    pd_value = db.Column(db.String(20))
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ==========================================
# 6. Prescription
# ==========================================
class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prescription_number = db.Column(db.String(50), unique=True) # Compatibility
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    eye_test_id = db.Column(db.Integer, db.ForeignKey('eye_test.id'), nullable=True)
    
    add_power = db.Column(db.String(20))
    prescription_image = db.Column(db.String(255))
    ai_extracted_text = db.Column(db.Text)
    confidence_score = db.Column(db.Float)
    doctor_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    date = db.Column(db.Date, default=datetime.utcnow) # Compatibility
    expiry_date = db.Column(db.Date) # Compatibility
    status = db.Column(db.String(20), default='Completed') # Compatibility
    
    eye_test = db.relationship('EyeTest', backref='prescriptions', uselist=False)

    def to_dict(self):
        # Flatten EyeTest into OD/OS object to preserve frontend compatibility perfectly
        et = self.eye_test
        return {
            "id": self.id, 
            "prescription_number": self.prescription_number,
            "customer_id": self.customer_id,
            "doctor_name": self.doctor_name,
            "date": str(self.date), 
            "expiry_date": str(self.expiry_date) if self.expiry_date else None,
            "status": self.status,
            "od": {
                "sph": et.right_sphere if et else None, 
                "cyl": et.right_cylinder if et else None, 
                "axis": et.right_axis if et else None, 
                "add": self.add_power,
                "pd": et.pd_value if et else None
            },
            "os": {
                "sph": et.left_sphere if et else None, 
                "cyl": et.left_cylinder if et else None, 
                "axis": et.left_axis if et else None, 
                "add": self.add_power,
                "pd": et.pd_value if et else None
            },
            "prescription_image": self.prescription_image,
            "ai_raw_text": self.ai_extracted_text,
            "confidence_score": self.confidence_score,
            "created_at": str(self.created_at) if self.created_at else None,
            "customer_name": f"{self.customer.first_name} {self.customer.last_name}" if self.customer else "Unknown"
        }

# ==========================================
# 7. Frame Inventory
# ==========================================
class Frame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    frame_code = db.Column(db.String(50), unique=True) # Compatibility
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    name = db.Column(db.String(150)) # Compatibility
    category = db.Column(db.String(50)) # Category: Eyeglasses, Sunglasses, Computer Glasses, Kids Glasses
    shape = db.Column(db.String(50))
    color = db.Column(db.String(50))
    size = db.Column(db.String(50))
    material = db.Column(db.String(50))
    gender = db.Column(db.String(20))
    price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float) # Compatibility
    stock = db.Column(db.Integer, default=0)
    min_stock = db.Column(db.Integer, default=5)
    image = db.Column(db.Text)
    vto_image = db.Column(db.Text) # For Virtual Try-On
    status = db.Column(db.String(50), default='Available') # Compatibility
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id, "frame_code": self.frame_code, "name": self.name or self.model,
            "brand": self.brand, "model": self.model, "brand_name": self.brand,
            "category": self.category or "Eyeglasses",
            "gender": self.gender, "shape": self.shape, "material": self.material,
            "size": self.size, "color": self.color, 
            "price": self.price, "selling_price": self.selling_price or self.price,
            "stock": self.stock, "min_stock": self.min_stock, 
            "status": self.status, "image": self.image, "vto_image": self.vto_image,
            "created_at": str(self.created_at)
        }

# ==========================================
# 8. Lens Inventory
# ==========================================
class Lens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lens_code = db.Column(db.String(50), unique=True) # Compatibility
    name = db.Column(db.String(150)) # Compatibility
    brand = db.Column(db.String(100))
    category = db.Column(db.String(50), default='Contact & Optical Lenses')
    type = db.Column(db.String(50)) # Single Vision, Progressive, Blue Cut, Anti Glare, Photochromic
    lens_type = db.Column(db.String(50)) # Compatibility
    coating = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float) # Compatibility
    stock = db.Column(db.Integer, default=0)
    min_stock = db.Column(db.Integer, default=10)
    image = db.Column(db.Text)
    status = db.Column(db.String(50), default='Available') # Compatibility
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id, "lens_code": self.lens_code, "name": self.name or f"{self.brand} {self.type}",
            "brand": self.brand, "brand_name": self.brand,
            "category": self.category or "Contact & Optical Lenses",
            "type": self.type, "lens_type": self.type or self.lens_type,
            "coating": self.coating, 
            "price": self.price, "selling_price": self.selling_price or self.price,
            "stock": self.stock, "min_stock": self.min_stock, 
            "status": self.status, "image": self.image,
            "created_at": str(self.created_at)
        }

# ==========================================
# 9. Supplier
# ==========================================
class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ==========================================
# 10. Orders & 11. Order Items
# ==========================================
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), unique=True)
    order_number = db.Column(db.String(50), unique=True) # Compatibility
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescription.id'), nullable=True)
    
    status = db.Column(db.String(50), default='Pending') # Pending, Processing, Ready, Delivered
    total_amount = db.Column(db.Float, default=0.0)
    
    order_date = db.Column(db.DateTime, default=datetime.utcnow) # Compatibility
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        valid_keys = {'id', 'order_id', 'order_number', 'customer_id', 'prescription_id', 'status', 'total_amount', 'order_date', 'created_at'}
        filtered = {k: v for k, v in kwargs.items() if k in valid_keys}
        super().__init__(**filtered)

    def to_dict(self):
        # We need to compute payment status for compatibility with older Billing module
        # A quick workaround: we just output standard fields.
        return {
            "id": self.id,
            "order_number": self.order_id or self.order_number,
            "customer_id": self.customer_id,
            "customer_name": f"{self.customer.first_name} {self.customer.last_name}" if self.customer else "Unknown",
            "prescription_id": self.prescription_id,
            "order_date": str(self.created_at),
            "status": self.status,
            "total_amount": self.total_amount,
            "created_at": str(self.created_at),
            "items": [item.to_dict() for item in self.items]
        }

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_type = db.Column(db.String(50)) # Frame, Lens
    item_type = db.Column(db.String(50)) # Compatibility
    product_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer) # Compatibility
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float)
    total_price = db.Column(db.Float) # Compatibility

    def __init__(self, **kwargs):
        if 'unit_price' in kwargs:
            kwargs['price'] = kwargs.pop('unit_price')
        if 'product_name' in kwargs:
            kwargs.pop('product_name')
        if 'item_name' in kwargs:
            kwargs.pop('item_name')
        if 'discount' in kwargs:
            kwargs.pop('discount')
        if 'gst' in kwargs:
            kwargs.pop('gst')
        super().__init__(**kwargs)

    @property
    def unit_price(self):
        return self.price

    @unit_price.setter
    def unit_price(self, val):
        self.price = val
    
    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "item_type": self.product_type or self.item_type,
            "item_id": self.product_id or self.item_id,
            "quantity": self.quantity,
            "unit_price": self.price,
            "total_price": (self.quantity * self.price) if self.price else self.total_price
        }

# ==========================================
# 12. Billing & 13. Payment
# ==========================================
class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    
    subtotal = db.Column(db.Float, default=0.0)
    discount = db.Column(db.Float, default=0.0)
    gst = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, nullable=False)
    
    payment_status = db.Column(db.String(20), default='Pending') # Paid, Pending
    payment_method = db.Column(db.String(50)) # Cash, Card, UPI
    
    invoice_pdf = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    order_rel = db.relationship('Order', backref=db.backref('billing', uselist=False))
    payments = db.relationship('Payment', backref='billing', lazy=True)

    def to_dict(self):
        # Flatten for UI compatibility
        return {
            "id": self.id,
            "invoice_number": self.invoice_number,
            "order_id": self.order_id,
            "customer_id": self.order_rel.customer_id if self.order_rel else None,
            "customer_name": f"{self.order_rel.customer.first_name} {self.order_rel.customer.last_name}" if self.order_rel and self.order_rel.customer else None,
            "subtotal": self.subtotal,
            "discount": self.discount,
            "gst_amount": self.gst,
            "total_amount": self.total_amount,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status,
            "created_at": str(self.created_at),
            "invoice_pdf": self.invoice_pdf
        }

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    billing_id = db.Column(db.Integer, db.ForeignKey('billing.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_id = db.Column(db.String(100))
    payment_method = db.Column(db.String(50))
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

# ==========================================
# 14. AI Recommendation Tables
# ==========================================
class LensRecommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescription.id'))
    recommended_lens = db.Column(db.Text)
    reason = db.Column(db.Text)
    ai_response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FrameRecommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    face_shape = db.Column(db.String(50))
    face_image = db.Column(db.String(255)) # Compatibility
    recommended_frames = db.Column(db.Text)
    selected_frame = db.Column(db.String(100))
    ai_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        import json
        frames = []
        try:
            if self.recommended_frames:
                frames = json.loads(self.recommended_frames)
        except:
            pass
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "face_shape": self.face_shape,
            "recommended_frames": frames,
            "ai_reason": self.ai_reason,
            "selected_frame": self.selected_frame,
            "created_at": str(self.created_at)
        }

# ==========================================
# 15. Virtual Try-On
# ==========================================
class VirtualTryOnHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    frame_id = db.Column(db.Integer, db.ForeignKey('frame.id'), nullable=False)
    original_image = db.Column(db.String(255))
    generated_image = db.Column(db.String(255))
    tryon_image = db.Column(db.String(255)) # Compatibility
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    frame = db.relationship('Frame')
    
    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "frame_id": self.frame_id,
            "frame_name": self.frame.name or self.frame.model if self.frame else "Unknown Frame",
            "tryon_image": self.tryon_image or self.generated_image,
            "created_at": str(self.created_at)
        }

# ==========================================
# 16. Chat History
# ==========================================
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True) # Compatibility
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User')
    customer = db.relationship('Customer')
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": self.user.username if self.user else "System",
            "customer_id": self.customer_id,
            "customer_name": f"{self.customer.first_name} {self.customer.last_name}" if self.customer else None,
            "question": self.question,
            "answer": self.answer,
            "created_at": str(self.created_at)
        }

# ==========================================
# 17. Notifications
# ==========================================
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)
    notification_type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Unread')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "notification_type": self.notification_type,
            "title": self.title,
            "message": self.message,
            "status": self.status,
            "created_at": str(self.created_at)
        }

# ==========================================
# 18. Audit Logs
# ==========================================
class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(100))
    module = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# ==========================================
# 19. Compatibility Models (Kept so frontend doesn't break)
# ==========================================
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class InventoryTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_type = db.Column(db.String(50))
    product_id = db.Column(db.Integer)
    transaction_type = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        if 'item_type' in kwargs:
            kwargs['product_type'] = kwargs.pop('item_type')
        if 'item_id' in kwargs:
            kwargs['product_id'] = kwargs.pop('item_id')
        if 'reason' in kwargs:
            kwargs['notes'] = kwargs.pop('reason')
        kwargs.pop('user_id', None)
        super().__init__(**kwargs)

    @property
    def item_type(self):
        return self.product_type
        
    @item_type.setter
    def item_type(self, val):
        self.product_type = val

    @property
    def item_id(self):
        return self.product_id

    @item_id.setter
    def item_id(self, val):
        self.product_id = val

    @property
    def reason(self):
        return self.notes

    @reason.setter
    def reason(self, val):
        self.notes = val

    def to_dict(self):
        return {
            "id": self.id,
            "product_type": self.product_type,
            "item_type": self.product_type,
            "product_id": self.product_id,
            "item_id": self.product_id,
            "transaction_type": self.transaction_type,
            "quantity": self.quantity,
            "reason": self.notes,
            "notes": self.notes,
            "date": str(self.created_at),
            "created_at": str(self.created_at)
        }

class OrderStatusHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    status = db.Column(db.String(50))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    order_rel = db.relationship('Order')

    def __init__(self, **kwargs):
        if 'remarks' in kwargs:
            kwargs['notes'] = kwargs.pop('remarks')
        if 'user_id' in kwargs:
            kwargs.pop('user_id')
        super().__init__(**kwargs)

    @property
    def remarks(self):
        return self.notes

    @remarks.setter
    def remarks(self, val):
        self.notes = val


