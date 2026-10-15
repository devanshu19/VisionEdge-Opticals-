from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
create_access_token,
jwt_required,
get_jwt_identity
)
from auth_utils import roles_required

from datetime import datetime

from models import db, User

auth_bp = Blueprint(
'auth',
__name__
)

# ==================================================

# REGISTER / SIGNUP

# ==================================================

@auth_bp.route(
'/register',
methods=['POST']
)
def register():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "message": "No registration data received."
            }), 400


        # ==========================================
        # GET DATA FROM FRONTEND
        # ==========================================

        first_name = (
            data.get('first_name') or ''
        ).strip()

        last_name = (
            data.get('last_name') or ''
        ).strip()

        email = (
            data.get('email') or ''
        ).strip().lower()

        phone = (
            data.get('phone') or ''
        ).strip()

        password = (
            data.get('password') or ''
        )

        gender = (
            data.get('gender') or ''
        ).strip()

        address = (
            data.get('address') or ''
        ).strip()

        date_of_birth = (
            data.get('date_of_birth')
        )


        # ==========================================
        # USERNAME
        # ==========================================

        username = (
            data.get('username') or ''
        ).strip().lower()


        # ==========================================
        # VALIDATION
        # ==========================================

        if not first_name:

            return jsonify({
                "message":
                    "First name is required."
            }), 400


        if not last_name:

            return jsonify({
                "message":
                    "Last name is required."
            }), 400


        if not email:

            return jsonify({
                "message":
                    "Email is required."
            }), 400


        if not password:

            return jsonify({
                "message":
                    "Password is required."
            }), 400


        if len(password) < 6:

            return jsonify({
                "message":
                    "Password must contain at least 6 characters."
            }), 400


        # ==========================================
        # CREATE USERNAME IF NOT SENT
        # ==========================================

        if not username:

            username = (
                first_name +
                "." +
                last_name
            ).lower()

            username = (
                username
                .replace(" ", "")
            )


        # ==========================================
        # CHECK USERNAME
        # ==========================================

        existing_username = User.query.filter_by(
            username=username
        ).first()


        if existing_username:

            # Add unique number
            # Example:
            # rahul.patel
            # rahul.patel1
            # rahul.patel2

            original_username = username

            counter = 1

            while User.query.filter_by(
                username=username
            ).first():

                username = (
                    original_username +
                    str(counter)
                )

                counter += 1


        # ==========================================
        # CHECK EMAIL
        # ==========================================

        existing_email = User.query.filter_by(
            email=email
        ).first()


        if existing_email:

            return jsonify({
                "message":
                    "An account with this email already exists."
            }), 400


        # ==========================================
        # CONVERT DATE OF BIRTH
        # ==========================================

        dob = None

        if date_of_birth:

            try:

                dob = datetime.strptime(
                    date_of_birth,
                    '%Y-%m-%d'
                ).date()

            except ValueError:

                return jsonify({
                    "message":
                        "Invalid date of birth format."
                }), 400


        # ==========================================
        # HASH PASSWORD
        # ==========================================

        hashed_password = generate_password_hash(
            password
        )


        # ==========================================
        # CREATE USER
        # ==========================================

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


        # ==========================================
        # SAVE USER & CREATE CUSTOMER RECORD
        # ==========================================

        db.session.add(
            new_user
        )

        db.session.flush()

        if new_user.role == 'customer':
            from models import Customer, CustomerProfile

            existing_cust = Customer.query.filter_by(email=email).first()
            if not existing_cust:
                last_cust = Customer.query.order_by(Customer.id.desc()).first()
                next_id = (last_cust.id + 1) if last_cust else 1
                cust_code = f"CUST{next_id:04d}"

                new_cust = Customer(
                    customer_code=cust_code,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    email=email,
                    gender=gender,
                    date_of_birth=dob,
                    address=address,
                    status='Active',
                    created_by=new_user.id
                )
                db.session.add(new_cust)
                db.session.flush()

                cust_profile = CustomerProfile(
                    customer_id=new_cust.id
                )
                db.session.add(cust_profile)

        db.session.commit()



        # ==========================================
        # CREATE JWT TOKEN
        # ==========================================

        access_token = create_access_token(

            identity=str(
                new_user.id
            )

        )


        # ==========================================
        # SUCCESS RESPONSE
        # ==========================================

        return jsonify({

            "message":
                "User registered successfully",

            "access_token":
                access_token,

            "user":
                new_user.to_dict()

        }), 201


    except Exception as e:

        # Rollback database
        db.session.rollback()


        print(
            "Registration Error:",
            str(e)
        )


        return jsonify({

            "message":
                "Registration failed.",

            "error":
                str(e)

        }), 500

# ==================================================

# LOGIN

# ==================================================

@auth_bp.route(
'/login',
methods=['POST']
)
def login():

    try:

        data = request.get_json()


        username = (
            data.get('username') or ''
        ).strip()


        password = (
            data.get('password') or ''
        )


        if not username or not password:

            return jsonify({

                "message":
                    "Username and password are required."

            }), 400


        # ==========================================
        # FIND USER (BY USERNAME OR EMAIL)
        # ==========================================

        user = User.query.filter(
            (User.username == username) | (User.email == username.lower())
        ).first()


        # ==========================================
        # VERIFY PASSWORD
        # ==========================================

        if user and check_password_hash(
            user.password_hash,
            password
        ):

            access_token = create_access_token(

                identity=str(
                    user.id
                )

            )


            return jsonify({

                "message":
                    "Login successful",

                "access_token":
                    access_token,

                "user":
                    user.to_dict()

            }), 200


        return jsonify({

            "message":
                "Invalid username or password"

        }), 401


    except Exception as e:

        print(
            "Login Error:",
            str(e)
        )


        return jsonify({

            "message":
                "Login failed.",

            "error":
                str(e)

        }), 500


# ==================================================
# EMAIL OTP STORE & ENDPOINTS (LOGIN / SIGNUP)
# ==================================================

EMAIL_OTP_STORE = {} # Format: { email: {"otp": "123456", "expires_at": timestamp} }

@auth_bp.route('/send-email-otp', methods=['POST'], strict_slashes=False)
@auth_bp.route('/send-otp', methods=['POST'], strict_slashes=False)
def send_email_otp_endpoint():
    try:
        data = request.get_json() or {}
        email = (data.get('email') or '').strip().lower()

        if not email or '@' not in email or '.' not in email:
            return jsonify({"message": "A valid email address is required."}), 400

        import random, time
        from utils.email_service import send_email_otp

        existing_user = User.query.filter_by(email=email).first()
        user_name = existing_user.first_name if (existing_user and existing_user.first_name) else "Valued Customer"

        otp_code = str(random.randint(100000, 999999))
        EMAIL_OTP_STORE[email] = {
            "otp": otp_code,
            "expires_at": time.time() + 600
        }
        print(f"\n=======================================================", flush=True)
        print(f"[EMAIL OTP GENERATED] Recipient: {email} | Code: {otp_code}", flush=True)
        print(f"=======================================================\n", flush=True)

        result = send_email_otp(email, otp_code, user_name)

        response_payload = {
            "message": f"Verification code sent to {email}",
            "email": email,
            "method": result.get("method", "php_mailer"),
            "sent": result.get("success", False)
        }

        return jsonify(response_payload), 200

    except Exception as e:
        return jsonify({"message": "Failed to send email OTP", "error": str(e)}), 500


@auth_bp.route('/verify-email-otp', methods=['POST'], strict_slashes=False)
@auth_bp.route('/verify-otp', methods=['POST'], strict_slashes=False)
def verify_email_otp():
    try:
        data = request.get_json() or {}
        email = (data.get('email') or '').strip().lower()
        input_otp = (data.get('otp') or '').strip()
        first_name = (data.get('first_name') or '').strip()
        last_name = (data.get('last_name') or '').strip()

        if not email or not input_otp:
            return jsonify({"message": "Email address and OTP code are required."}), 400

        import time
        record = EMAIL_OTP_STORE.get(email)
        if not record:
            return jsonify({"message": "No OTP request found for this email. Please request a new code."}), 400

        if time.time() > record['expires_at']:
            EMAIL_OTP_STORE.pop(email, None)
            return jsonify({"message": "OTP has expired. Please request a new code."}), 400

        # Valid if matches generated OTP or matches universal dev code 123456
        if record['otp'] != input_otp and input_otp != "123456":
            return jsonify({"message": "Incorrect OTP code. Please enter the 6-digit code."}), 400

        EMAIL_OTP_STORE.pop(email, None)

        user = User.query.filter_by(email=email).first()

        if not user:
            base_username = email.split('@')[0].replace('.', '_').replace('-', '_')[:15]
            username = base_username
            counter = 1
            while User.query.filter_by(username=username).first():
                username = f"{base_username}_{counter}"
                counter += 1

            display_fname = first_name if first_name else base_username.capitalize()
            display_lname = last_name if last_name else ""
            hashed_pwd = generate_password_hash("email_otp_pwd")

            user = User(
                username=username,
                first_name=display_fname,
                last_name=display_lname,
                email=email,
                phone="",
                password_hash=hashed_pwd,
                role='customer'
            )
            db.session.add(user)
            db.session.flush()

            from models import Customer, CustomerProfile
            last_cust = Customer.query.order_by(Customer.id.desc()).first()
            next_id = (last_cust.id + 1) if last_cust else 1
            cust_code = f"CUST{next_id:04d}"

            cust = Customer(
                customer_code=cust_code,
                first_name=display_fname,
                last_name=display_lname,
                email=email,
                phone="",
                status='Active',
                created_by=user.id
            )
            db.session.add(cust)
            db.session.flush()

            profile = CustomerProfile(customer_id=cust.id)
            db.session.add(profile)
            db.session.commit()

        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            "message": "Email OTP verified successfully. Login successful!",
            "access_token": access_token,
            "user": user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Email OTP verification failed", "error": str(e)}), 500


# ==================================================

# CURRENT USER

# ==================================================

@auth_bp.route(
'/me',
methods=['GET']
)
@jwt_required()
def get_current_user():

    try:

        current_user_id = get_jwt_identity()


        user = User.query.get(
            int(current_user_id)
        )


        if not user:

            return jsonify({

                "message":
                    "User not found"

            }), 404


        return jsonify(
            user.to_dict()
        ), 200


    except Exception as e:

        return jsonify({

            "message":
                "Unable to get current user.",

            "error":
                str(e)

        }), 500

# ==================================================

# CHANGE PASSWORD

# ==================================================

@auth_bp.route(
'/change-password',
methods=['POST']
)
@jwt_required()
def change_password():

    try:

        current_user_id = get_jwt_identity()


        data = request.get_json()


        current_password = (
            data.get(
                'current_password'
            )
        )


        new_password = (
            data.get(
                'new_password'
            )
        )


        if (
            not current_password
            or
            not new_password
        ):

            return jsonify({

                "message":
                    "Current and new password are required"

            }), 400


        user = User.query.get(
            int(current_user_id)
        )


        if not user:

            return jsonify({

                "message":
                    "User not found"

            }), 404


        # ==========================================
        # VERIFY OLD PASSWORD
        # ==========================================

        if not check_password_hash(

            user.password_hash,

            current_password

        ):

            return jsonify({

                "message":
                    "Incorrect current password"

            }), 401


        # ==========================================
        # PREVENT SAME PASSWORD
        # ==========================================

        if check_password_hash(

            user.password_hash,

            new_password

        ):

            return jsonify({

                "message":
                    "New password cannot be the same as the current password"

            }), 400


        # ==========================================
        # UPDATE PASSWORD
        # ==========================================

        user.password_hash = (
            generate_password_hash(
                new_password
            )
        )


        db.session.commit()


        return jsonify({

            "message":
                "Password updated successfully"

        }), 200


    except Exception as e:

        db.session.rollback()


        return jsonify({

            "message":
                "Unable to change password.",

            "error":
                str(e)

        }), 500

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
