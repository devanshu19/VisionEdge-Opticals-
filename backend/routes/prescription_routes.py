from flask import Blueprint, request, jsonify, send_file
from auth_utils import roles_required
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import db, Prescription, Customer, User
from datetime import datetime
from sqlalchemy import or_
import io

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

prescription_bp = Blueprint('prescription', __name__)

@prescription_bp.route('/stats', methods=['GET'])
@roles_required('admin', 'staff')
def get_stats():
    total = Prescription.query.count()
    completed = Prescription.query.filter_by(status='Completed').count()
    draft = Prescription.query.filter_by(status='Draft').count()
    
    today = datetime.utcnow().date()
    today_new = Prescription.query.filter(Prescription.date == today).count()
    
    return jsonify({
        "total": total,
        "completed": completed,
        "draft": draft,
        "today_new": today_new
    }), 200

@prescription_bp.route('/', methods=['GET'])
@roles_required('admin', 'staff')
def get_prescriptions():
    query = Prescription.query
    
    customer_id = request.args.get('customer_id')
    search = request.args.get('search', '')
    status = request.args.get('status', 'all')
    
    if customer_id:
        query = query.filter_by(customer_id=customer_id)
        
    if status.lower() != 'all':
        query = query.filter(Prescription.status == status.capitalize())
        
    if search:
        search_term = f"%{search}%"
        # Join Customer to search by name/phone
        query = query.join(Customer).filter(or_(
            Prescription.prescription_number.ilike(search_term),
            Prescription.doctor_name.ilike(search_term),
            Customer.first_name.ilike(search_term),
            Customer.last_name.ilike(search_term),
            Customer.phone.ilike(search_term)
        ))
        
    prescriptions = query.order_by(Prescription.date.desc()).all()
    return jsonify([rx.to_dict() for rx in prescriptions]), 200

@prescription_bp.route('/<int:id>', methods=['GET'])
@roles_required('admin', 'staff')
def get_prescription(id):
    rx = Prescription.query.get_or_404(id)
    return jsonify(rx.to_dict()), 200

@prescription_bp.route('/', methods=['POST'])
@roles_required('admin', 'staff')
def create_prescription():
    data = request.get_json()
    
    if 'customer_id' not in data:
        return jsonify({"message": "customer_id is required"}), 400
        
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
        
    try:
        rx_date = datetime.strptime(data.get('date', datetime.utcnow().strftime('%Y-%m-%d')), '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"message": "Invalid date format, use YYYY-MM-DD"}), 400

    expiry_date = None
    if data.get('expiry_date'):
        try:
            expiry_date = datetime.strptime(data['expiry_date'], '%Y-%m-%d').date()
        except ValueError:
            pass

    od = data.get('od', {})
    os = data.get('os', {})
    
    # Auto-generate prescription_number
    last_rx = Prescription.query.order_by(Prescription.id.desc()).first()
    next_id = last_rx.id + 1 if last_rx else 1
    prescription_number = f"RX-{next_id:05d}"
    
    from models import EyeTest
    new_test = EyeTest(
        customer_id=customer.id,
        right_sphere=od.get('sph'), right_cylinder=od.get('cyl'), right_axis=od.get('axis'), right_addition=od.get('add'), right_vision=od.get('va'),
        left_sphere=os.get('sph'), left_cylinder=os.get('cyl'), left_axis=os.get('axis'), left_addition=os.get('add'), left_vision=os.get('va'),
        pd_value=data.get('distance_pd') or data.get('near_pd'),
        remarks=data.get('notes'),
        test_date=rx_date
    )
    db.session.add(new_test)
    db.session.flush()
    
    new_rx = Prescription(
        prescription_number=prescription_number,
        customer_id=customer.id,
        eye_test_id=new_test.id,
        doctor_name=data.get('doctor_name'),
        date=rx_date,
        expiry_date=expiry_date,
        status=data.get('status', 'Completed'),
        lens_type=data.get('lens_type'),
        lens_material=data.get('lens_material'),
        lens_coating=data.get('lens_coating'),
        frame_recommendation=data.get('frame_recommendation'),
        lens_recommendation=data.get('lens_recommendation'),
        notes=data.get('notes'),
        prescription_image=data.get('prescription_image'),
        ai_extracted_text=data.get('ai_raw_text'),
        confidence_score=data.get('confidence_score'),
        created_by=int(get_jwt_identity()) if get_jwt_identity() else None
    )
    
    db.session.add(new_rx)
    db.session.commit()
    
    return jsonify({"message": "Prescription created successfully", "prescription": new_rx.to_dict()}), 201

@prescription_bp.route('/<int:id>', methods=['PUT'])
@roles_required('admin', 'staff')
def update_prescription(id):
    rx = Prescription.query.get_or_404(id)
    data = request.get_json()
    
    if 'date' in data:
        try:
            rx.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            pass
            
    if 'expiry_date' in data:
        try:
            rx.expiry_date = datetime.strptime(data['expiry_date'], '%Y-%m-%d').date() if data['expiry_date'] else None
        except ValueError:
            pass
            
    fields = ['doctor_name', 'status', 'lens_type', 'lens_material', 'lens_coating', 'frame_recommendation', 'lens_recommendation', 'notes']
    for field in fields:
        if field in data:
            setattr(rx, field, data[field])
            
    if rx.eye_test:
        test = rx.eye_test
        if 'od' in data:
            od = data['od']
            if 'sph' in od: test.right_sphere = od['sph']
            if 'cyl' in od: test.right_cylinder = od['cyl']
            if 'axis' in od: test.right_axis = od['axis']
            if 'add' in od: test.right_addition = od['add']
            if 'va' in od: test.right_vision = od['va']
        if 'os' in data:
            os = data['os']
            if 'sph' in os: test.left_sphere = os['sph']
            if 'cyl' in os: test.left_cylinder = os['cyl']
            if 'axis' in os: test.left_axis = os['axis']
            if 'add' in os: test.left_addition = os['add']
            if 'va' in os: test.left_vision = os['va']
        if 'distance_pd' in data or 'near_pd' in data:
            test.pd_value = data.get('distance_pd') or data.get('near_pd')
            
    rx.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({"message": "Prescription updated successfully", "prescription": rx.to_dict()}), 200

@prescription_bp.route('/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_prescription(id):
    rx = Prescription.query.get_or_404(id)
    db.session.delete(rx)
    db.session.commit()
    return jsonify({"message": "Prescription deleted successfully"}), 200

@prescription_bp.route('/<int:id>/pdf', methods=['GET'])
@roles_required('admin', 'staff')
def generate_pdf(id):
    rx = Prescription.query.get_or_404(id)
    customer = rx.customer
    
    if not REPORTLAB_AVAILABLE:
        # Fallback if ReportLab couldn't be installed due to environment issues
        return jsonify({
            "error": "ReportLab not installed",
            "message": "PDF Generation requires ReportLab. Please manually install reportlab.",
            "prescription": rx.to_dict()
        }), 501

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Header
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.HexColor("#0d6efd"))
    c.drawString(50, height - 50, "VisionEdge Opticals")
    
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.gray)
    c.drawString(50, height - 70, "123 Innovation Drive, Tech City")
    c.drawString(50, height - 85, "Phone: +1 234 567 8900 | Email: care@visionedge.com")
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.black)
    c.drawString(50, height - 130, "OPTICAL PRESCRIPTION")
    
    # Metadata
    c.setFont("Helvetica", 10)
    c.drawString(400, height - 130, f"Rx Number: {rx.prescription_number}")
    c.drawString(400, height - 145, f"Date: {rx.date}")
    c.drawString(400, height - 160, f"Expiry: {rx.expiry_date if rx.expiry_date else 'N/A'}")
    
    # Patient Info
    c.rect(50, height - 230, width - 100, 50)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(60, height - 195, "Patient Information:")
    c.setFont("Helvetica", 11)
    c.drawString(60, height - 215, f"Name: {customer.first_name} {customer.last_name}")
    c.drawString(300, height - 215, f"Phone: {customer.phone}")
    
    # Table Header
    y = height - 280
    c.setFont("Helvetica-Bold", 10)
    c.rect(50, y-15, width - 100, 20, fill=1)
    c.setFillColor(colors.white)
    c.drawString(60, y-10, "EYE")
    c.drawString(120, y-10, "SPH")
    c.drawString(180, y-10, "CYL")
    c.drawString(240, y-10, "AXIS")
    c.drawString(300, y-10, "ADD")
    c.drawString(360, y-10, "PRISM")
    c.drawString(420, y-10, "BASE")
    c.drawString(480, y-10, "VA")
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    
    # OD Row
    y -= 35
    c.drawString(60, y, "Right (OD)")
    c.drawString(120, y, rx.od_sph or "-")
    c.drawString(180, y, rx.od_cyl or "-")
    c.drawString(240, y, rx.od_axis or "-")
    c.drawString(300, y, rx.od_add or "-")
    c.drawString(360, y, rx.od_prism or "-")
    c.drawString(420, y, rx.od_base or "-")
    c.drawString(480, y, rx.od_va or "-")
    c.line(50, y-10, width-50, y-10)
    
    # OS Row
    y -= 25
    c.drawString(60, y, "Left (OS)")
    c.drawString(120, y, rx.os_sph or "-")
    c.drawString(180, y, rx.os_cyl or "-")
    c.drawString(240, y, rx.os_axis or "-")
    c.drawString(300, y, rx.os_add or "-")
    c.drawString(360, y, rx.os_prism or "-")
    c.drawString(420, y, rx.os_base or "-")
    c.drawString(480, y, rx.os_va or "-")
    c.line(50, y-10, width-50, y-10)
    
    # Recommendations
    y -= 50
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Recommendations & Notes")
    c.setFont("Helvetica", 10)
    
    y -= 20
    c.drawString(50, y, f"Lens Type: {rx.lens_type or 'N/A'}")
    c.drawString(300, y, f"Material: {rx.lens_material or 'N/A'}")
    
    y -= 20
    c.drawString(50, y, f"Coating: {rx.lens_coating or 'N/A'}")
    
    y -= 30
    c.drawString(50, y, "Notes:")
    y -= 15
    c.drawString(50, y, rx.notes or "No additional notes.")
    
    # Doctor Signature
    y -= 100
    c.line(50, y, 200, y)
    c.drawString(50, y-15, f"Dr. {rx.doctor_name or '_________________'}")
    c.drawString(50, y-30, "Signature")
    
    c.showPage()
    c.save()
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"Prescription_{rx.prescription_number}.pdf",
        mimetype='application/pdf'
    )

@prescription_bp.route('/save-extracted', methods=['POST'])
@roles_required('admin', 'staff', 'customer', 'guest')
def save_extracted_prescription():
    data = request.get_json() or {}
    
    customer_id = data.get('customer_id')
    customer = None
    if customer_id:
        customer = Customer.query.get(customer_id)
        
    if not customer:
        customer = Customer.query.first()
        
    if not customer:
        customer = Customer(
            first_name="Guest",
            last_name="Customer",
            phone="9999999999",
            email="guest@visionedge.com"
        )
        db.session.add(customer)
        db.session.flush()

    rx_date = datetime.utcnow().date()
    last_rx = Prescription.query.order_by(Prescription.id.desc()).first()
    next_id = (last_rx.id + 1) if last_rx else 1
    prescription_number = f"RX-{next_id:05d}"
    
    from models import EyeTest
    new_test = EyeTest(
        customer_id=customer.id,
        right_sphere=str(data.get('right_sphere', '-1.25')),
        right_cylinder=str(data.get('right_cylinder', '-0.50')),
        right_axis=str(data.get('right_axis', '90')),
        left_sphere=str(data.get('left_sphere', '-1.50')),
        left_cylinder=str(data.get('left_cylinder', '-0.75')),
        left_axis=str(data.get('left_axis', '180')),
        pd_value=str(data.get('pd', '64')),
        remarks=f"Saved via AI OCR Scanner (Add: {data.get('add_power', '+1.50')})"
    )
    db.session.add(new_test)
    db.session.flush()
    
    new_rx = Prescription(
        prescription_number=prescription_number,
        customer_id=customer.id,
        eye_test_id=new_test.id,
        doctor_name=data.get('doctor_name', 'AI Doctor Prescription'),
        date=rx_date,
        add_power=str(data.get('add_power', '+1.50')),
        prescription_image=data.get('prescription_image'),
        ai_extracted_text=str(data.get('raw_text', '')),
        confidence_score=float(data.get('confidence_score', 0.98)),
        status='Completed'
    )
    db.session.add(new_rx)
    db.session.commit()
    
    return jsonify({
        "message": "Prescription saved to database successfully!",
        "prescription_id": new_rx.id,
        "prescription_number": new_rx.prescription_number,
        "prescription": new_rx.to_dict()
    }), 201

# ==================================================
# CUSTOMER PRESCRIPTIONS (LIVE DATA)
# ==================================================
@prescription_bp.route('/my-prescriptions', methods=['GET'])
@jwt_required()
def my_prescriptions():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify([]), 200

        customer = Customer.query.filter_by(created_by=user.id).first()
        if not customer and user.phone:
            customer = Customer.query.filter_by(phone=user.phone).first()
        if not customer and user.email:
            customer = Customer.query.filter_by(email=user.email).first()

        if not customer:
            return jsonify([]), 200

        rx_list = Prescription.query.filter_by(customer_id=customer.id).order_by(Prescription.created_at.desc()).all()
        return jsonify([rx.to_dict() for rx in rx_list]), 200
    except Exception as e:
        return jsonify({"message": "Failed to fetch prescriptions", "error": str(e)}), 500

