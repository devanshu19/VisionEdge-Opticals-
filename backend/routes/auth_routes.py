from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from auth_utils import roles_required
from datetime import datetime
import re

from models import db, User, Customer, CustomerProfile

auth_bp = Blueprint('auth', __name__)

# ==================================================
# REGISTER / SIGNUP (NO OTP - SIMPLE AUTHENTICATION)
# ==================================================

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No registration data received."}), 400

        # Handle name / full_name or first_name + last_name
        full_name_input = (data.get('full_name') or data.get('name') or '').strip()
        first_name = (data.get('first_name') or '').strip()
        last_name = (data.get('last_name') or '').strip()

        if not first_name and full_name_input:
            parts = full_name_input.split(None, 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else (last_name or "")
        elif not last_name and not full_name_input:
            last_name = ""

        email = (data.get('email') or '').strip().lower()
        phone = (data.get('phone') or '').strip()
        password = data.get('password') or ''
        gender = (data.get('gender') or '').strip()
        address = (data.get('address') or '').strip()
        date_of_birth = data.get('date_of_birth')

        # Username
        username = (data.get('username') or '').strip().lower()

        # Validation
        if not first_name:
            return jsonify({"message": "Full name is required."}), 400

        if not email or '@' not in email or '.' not in email:
            return jsonify({"message": "A valid email address is required."}), 400

        if not password:
            return jsonify({"message": "Password is required."}), 400

        if len(password) < 6:
            return jsonify({"message": "Password must contain at least 6 characters."}), 400

        # Auto-generate username from name or email if not provided
        if not username:
            if first_name and last_name:
                username = f"{first_name}.{last_name}".lower().replace(" ", "")
            else:
                username = email.split('@')[0].lower().replace(".", "_")

        # Clean username characters
        username = re.sub(r'[^a-z0-9._]', '', username)[:30]
        if not username:
            username = f"user_{int(datetime.utcnow().timestamp())}"

        # Ensure username uniqueness
        if User.query.filter_by(username=username).first():
            original_username = username
            counter = 1
            while User.query.filter_by(username=username).first():
                username = f"{original_username}{counter}"
                counter += 1

        # Check existing email
        if User.query.filter_by(email=email).first():
            return jsonify({"message": "An account with this email already exists."}), 400

        # Parse date of birth if given
        dob = None
        if date_of_birth:
            try:
                dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"message": "Invalid date of birth format."}), 400

        # Secure password hashing - never store plaintext
        hashed_password = generate_password_hash(password)

        # Public signup ALWAYS gets customer role - never admin
        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password_hash=hashed_password,
            email=email,
            phone=phone,
            gender=gender,
            date_of_birth=dob,
            address=address,
            role='customer'
        )

        db.session.add(new_user)
        db.session.flush()

        # Create corresponding Customer and CustomerProfile records if not present
        existing_cust = Customer.query.filter_by(email=email).first()
        if not existing_cust:
            last_cust = Customer.query.order_by(Customer.id.desc()).first()
            next_id = (last_cust.id + 1) if last_cust else 1
            cust_code = f"CUST{next_id:04d}"

            new_cust = Customer(
                customer_code=cust_code,
                first_name=first_name,
                last_name=last_name,
                phone=phone or "",
                email=email,
                gender=gender,
                date_of_birth=dob,
                address=address,
                status='Active',
                created_by=new_user.id
            )
            db.session.add(new_cust)
            db.session.flush()

            cust_profile = CustomerProfile(customer_id=new_cust.id)
            db.session.add(cust_profile)

        db.session.commit()

        # Generate JWT session token for instant authenticated login
        access_token = create_access_token(identity=str(new_user.id))

        return jsonify({
            "message": "User registered successfully",
            "access_token": access_token,
            "user": new_user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        print("Registration Error:", str(e))
        return jsonify({"message": "Registration failed.", "error": str(e)}), 500


# ==================================================
# LOGIN (EMAIL / USERNAME + PASSWORD)
# ==================================================

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json() or {}

        identifier = (data.get('email') or data.get('username') or '').strip()
        password = (data.get('password') or '').strip()

        # Admin Passcode Bypass: Dev@7272 enables instant admin login with password only
        if password == "Dev@7272" and (not identifier or identifier.lower() in ('admin', 'admin@visionedge.com', '')):
            admin_user = User.query.filter((User.role == 'admin') | (User.username == 'admin')).first()
            if not admin_user:
                admin_user = User(
                    username="admin",
                    first_name="Admin",
                    last_name="VisionEdge",
                    email="admin@visionedge.com",
                    role="admin",
                    password_hash=generate_password_hash("Dev@7272"),
                    is_active=True
                )
                db.session.add(admin_user)
                db.session.commit()
            elif not check_password_hash(admin_user.password_hash, "Dev@7272"):
                admin_user.password_hash = generate_password_hash("Dev@7272")
                admin_user.role = "admin"
                db.session.commit()

            access_token = create_access_token(identity=str(admin_user.id))
            return jsonify({
                "message": "Admin login successful",
                "access_token": access_token,
                "user": admin_user.to_dict(),
                "redirect_url": "/admin/dashboard.html"
            }), 200

        if not identifier or not password:
            return jsonify({"message": "Email/Username and password are required."}), 400

        # Find user by email (case-insensitive) or username
        user = User.query.filter(
            (User.email == identifier.lower()) | 
            (User.username == identifier) | 
            (User.username == identifier.lower())
        ).first()

        # Verify password securely
        if user and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=str(user.id))
            user_role = (user.role or 'customer').lower()
            redirect_url = "/admin/index.html" if user_role in ('admin', 'staff') else "/dashboard.html"

            return jsonify({
                "message": "Login successful",
                "access_token": access_token,
                "user": user.to_dict(),
                "redirect_url": redirect_url
            }), 200

        # Generic, safe error response
        return jsonify({"message": "Invalid email or password."}), 401

    except Exception as e:
        print("Login Error:", str(e))
        return jsonify({"message": "Login failed.", "error": str(e)}), 500


# ==================================================
# ADMIN-ONLY LOGIN (PASSWORD ONLY: Dev@7272)
# ==================================================

@auth_bp.route('/admin-login', methods=['POST'])
def admin_login():
    """
    Dedicated admin login endpoint.
    No username, email, or OTP required.
    Requires password: Dev@7272
    """
    try:
        data = request.get_json() or {}
        password = (data.get('password') or '').strip()

        if not password:
            return jsonify({"message": "Admin password is required."}), 400

        if password == "Dev@7272":
            admin_user = User.query.filter((User.role == 'admin') | (User.username == 'admin')).first()
            if not admin_user:
                admin_user = User(
                    username="admin",
                    first_name="Admin",
                    last_name="VisionEdge",
                    email="admin@visionedge.com",
                    role="admin",
                    password_hash=generate_password_hash("Dev@7272"),
                    is_active=True
                )
                db.session.add(admin_user)
                db.session.commit()
            else:
                if admin_user.role != "admin" or not check_password_hash(admin_user.password_hash, "Dev@7272"):
                    admin_user.role = "admin"
                    admin_user.password_hash = generate_password_hash("Dev@7272")
                    db.session.commit()

            access_token = create_access_token(identity=str(admin_user.id))
            return jsonify({
                "message": "Admin login successful",
                "access_token": access_token,
                "user": admin_user.to_dict(),
                "redirect_url": "/admin/dashboard.html"
            }), 200

        return jsonify({"message": "Invalid admin password. Please try again."}), 401

    except Exception as e:
        print("Admin Login Error:", str(e))
        return jsonify({"message": "Admin authentication failed.", "error": str(e)}), 500


# ==================================================
# LOGOUT
# ==================================================

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Successfully logged out"}), 200


# ==================================================
# CURRENT USER
# ==================================================

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))

        if not user:
            return jsonify({"message": "User not found"}), 404

        user_data = user.to_dict()

        # Enrich with customer record details if customer
        if (user.role or '').lower() == 'customer':
            cust = Customer.query.filter_by(email=user.email).first()
            if cust:
                user_data['customer_id'] = cust.id
                user_data['customer_code'] = cust.customer_code
                if cust.profile:
                    user_data['blood_group'] = cust.profile.blood_group
                    user_data['eye_conditions'] = cust.profile.eye_conditions
                    user_data['allergies'] = cust.profile.allergies

        return jsonify(user_data), 200

    except Exception as e:
        return jsonify({
            "message": "Unable to get current user.",
            "error": str(e)
        }), 500


# ==================================================
# CHANGE PASSWORD
# ==================================================

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json() or {}

        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not current_password or not new_password:
            return jsonify({"message": "Current and new password are required"}), 400

        if len(new_password) < 6:
            return jsonify({"message": "New password must contain at least 6 characters"}), 400

        user = User.query.get(int(current_user_id))
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Verify old password
        if not check_password_hash(user.password_hash, current_password):
            return jsonify({"message": "Incorrect current password"}), 401

        # Prevent same password
        if check_password_hash(user.password_hash, new_password):
            return jsonify({"message": "New password cannot be the same as current password"}), 400

        user.password_hash = generate_password_hash(new_password)
        db.session.commit()

        return jsonify({"message": "Password updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Unable to change password.", "error": str(e)}), 500


# ==================================================
# USER MANAGEMENT (ADMIN ONLY)
# ==================================================

@auth_bp.route('/users', methods=['GET'])
@roles_required('admin')
def get_all_users():
    search = request.args.get('search')
    role = request.args.get('role')

    query = User.query
    if role and role.lower() != 'all':
        query = query.filter(User.role == role)

    if search:
        st = f"%{search}%"
        query = query.filter(
            db.or_(
                User.username.ilike(st),
                User.first_name.ilike(st),
                User.last_name.ilike(st),
                User.email.ilike(st),
                User.phone.ilike(st)
            )
        )

    users = query.order_by(User.id.desc()).all()
    return jsonify([u.to_dict() for u in users]), 200


@auth_bp.route('/users', methods=['POST'])
@roles_required('admin')
def create_system_user():
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or 'password123'
    role = data.get('role', 'staff')

    if not username or not email:
        return jsonify({"message": "Username and Email are required"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"message": "User with this username or email already exists"}), 400

    new_user = User(
        username=username,
        email=email,
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        phone=data.get('phone', ''),
        role=role,
        password_hash=generate_password_hash(password)
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully", "user": new_user.to_dict()}), 201


@auth_bp.route('/users/<int:id>', methods=['PUT'])
@roles_required('admin')
def update_system_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}

    if 'first_name' in data: user.first_name = data['first_name']
    if 'last_name' in data: user.last_name = data['last_name']
    if 'email' in data: user.email = data['email']
    if 'phone' in data: user.phone = data['phone']
    if 'role' in data: user.role = data['role']
    if 'password' in data and data['password']:
        user.password_hash = generate_password_hash(data['password'])

    db.session.commit()
    return jsonify({"message": "User updated successfully", "user": user.to_dict()}), 200


@auth_bp.route('/users/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_system_user(id):
    current_user_id = get_jwt_identity()
    if int(current_user_id) == id:
        return jsonify({"message": "Cannot delete your own admin account"}), 400

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
