from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    role = db.Column(db.String(50), default='admin')
    
    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email, "role": self.role}

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    gender = db.Column(db.String(10))
    dob = db.Column(db.Date)
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    prescriptions = db.relationship('Prescription', backref='customer', lazy=True, cascade="all, delete-orphan")
    invoices = db.relationship('Invoice', backref='customer', lazy=True)

    def to_dict(self):
        return {
            "id": self.id, "first_name": self.first_name, "last_name": self.last_name,
            "phone": self.phone, "email": self.email, "gender": self.gender, 
            "dob": str(self.dob) if self.dob else None, "address": self.address,
            "created_at": str(self.created_at)
        }

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date)
    
    od_sph = db.Column(db.String(10))
    od_cyl = db.Column(db.String(10))
    od_axis = db.Column(db.String(10))
    od_add = db.Column(db.String(10))
    od_pd = db.Column(db.String(10))
    
    os_sph = db.Column(db.String(10))
    os_cyl = db.Column(db.String(10))
    os_axis = db.Column(db.String(10))
    os_add = db.Column(db.String(10))
    os_pd = db.Column(db.String(10))
    
    notes = db.Column(db.Text)
    
    def to_dict(self):
        return {
            "id": self.id, "customer_id": self.customer_id,
            "date": str(self.date), "expiry_date": str(self.expiry_date) if self.expiry_date else None,
            "od": {"sph": self.od_sph, "cyl": self.od_cyl, "axis": self.od_axis, "add": self.od_add, "pd": self.od_pd},
            "os": {"sph": self.os_sph, "cyl": self.os_cyl, "axis": self.os_axis, "add": self.os_add, "pd": self.os_pd},
            "notes": self.notes
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50))
    stock = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id, "item_code": self.item_code, "name": self.name,
            "category": self.category, "brand": self.brand, "stock": self.stock, "price": self.price
        }

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    subtotal = db.Column(db.Float, default=0.0)
    discount = db.Column(db.Float, default=0.0)
    gst = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending')
    
    items = db.relationship('InvoiceItem', backref='invoice', lazy=True, cascade="all, delete-orphan")
    payments = db.relationship('Payment', backref='invoice', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id, "invoice_number": self.invoice_number, "customer_id": self.customer_id,
            "subtotal": self.subtotal, "discount": self.discount, "gst": self.gst, "total": self.total,
            "date": str(self.date), "status": self.status,
            "items": [item.to_dict() for item in self.items]
        }

class InvoiceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    description = db.Column(db.String(150))
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id, "product_id": self.product_id, "description": self.description,
            "quantity": self.quantity, "price": self.price
        }

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_mode = db.Column(db.String(50)) # Cash, Card, UPI
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id, "invoice_id": self.invoice_id, "amount": self.amount,
            "payment_mode": self.payment_mode, "date": str(self.date)
        }
