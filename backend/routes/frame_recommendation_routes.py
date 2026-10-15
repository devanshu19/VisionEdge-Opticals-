from flask import Blueprint, request, jsonify, current_app
from auth_utils import roles_required
from flask_jwt_extended import get_jwt_identity
from models import db, FrameRecommendation, Customer, Frame, Brand
from utils.face_analysis import detect_face_shape
from utils.frame_ai import recommend_frames_ai
from werkzeug.utils import secure_filename
import os
import uuid

recommendation_bp = Blueprint('recommendation', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@recommendation_bp.route('/analyze-face', methods=['POST'])
@roles_required('admin', 'staff', 'customer', 'guest')
def analyze_face():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Generate unique name
        ext = filename.rsplit('.', 1)[1].lower()
        unique_name = f"{uuid.uuid4().hex}.{ext}"
        
        # Ensure media/faces directory exists
        upload_folder = os.path.join(current_app.root_path, 'media', 'faces')
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, unique_name)
        file.save(filepath)
        
        # Call Face Analysis module
        result = detect_face_shape(filepath)
        
        if result['success']:
            image_url = f"/api/media/faces/{unique_name}"
            return jsonify({
                "message": "Face analyzed successfully",
                "face_shape": result['face_shape'],
                "confidence": result['confidence'],
                "image_url": image_url,
                "is_mock": result['is_mock']
            }), 200
        else:
            return jsonify({"message": result['message']}), 400
            
    return jsonify({"message": "Invalid file type"}), 400

@recommendation_bp.route('/generate', methods=['POST'])
@roles_required('admin', 'staff', 'customer', 'guest')
def generate_recommendation():
    data = request.get_json() or {}
    
    customer_id = data.get('customer_id')
    face_shape = data.get('face_shape')
    budget = data.get('budget', 'Any')
    usage = data.get('usage', 'Any')
    size = data.get('size', 'Any')
    
    if not face_shape:
        return jsonify({"message": "face_shape is required"}), 400
        
    customer = Customer.query.get(customer_id) if customer_id else None
    
    customer_data = {
        "age": customer.to_dict().get('age') if customer else 30,
        "gender": customer.gender if customer else "Any",
        "budget": budget,
        "usage": usage,
        "size": size
    }
    
    # Fetch inventory frames with stock > 0
    # Also fetch the Brand name directly through relationship mapping
    available_frames = Frame.query.filter(Frame.stock > 0).all()
    
    inventory_data = []
    for f in available_frames:
        brand_name = f.brand if (isinstance(f.brand, str) and f.brand) else (getattr(f.brand, 'name', None) or "Unknown")
        inventory_data.append({
            "id": f.id,
            "name": f.name,
            "brand": brand_name,
            "shape": f.shape,
            "color": f.color,
            "price": f.selling_price,
            "stock": f.stock,
            "image": f.image
        })
        
    # Call AI
    ai_result = recommend_frames_ai(customer_data, face_shape, inventory_data)
    
    if not ai_result['success']:
        return jsonify({"message": "AI failed to generate recommendation"}), 500
        
    # Combine the actual frames data from the IDs returned by AI
    ai_data = ai_result['data']
    selected_ids = set(ai_data.get('selected_inventory_ids', []))
    
    recommended_actual_frames = []
    for item in inventory_data:
        if item['id'] in selected_ids:
            recommended_actual_frames.append(item)
            
    return jsonify({
        "message": "Recommendation generated",
        "ai_analysis": ai_data,
        "recommended_frames": recommended_actual_frames,
        "is_mock": ai_result['is_mock']
    }), 200

@recommendation_bp.route('/save', methods=['POST'])
@roles_required('admin', 'staff')
def save_recommendation():
    data = request.get_json()
    
    import json
    
    try:
        rec = FrameRecommendation(
            customer_id=data['customer_id'],
            face_shape=data['face_shape'],
            face_image=data.get('face_image'),
            recommended_frames=json.dumps(data.get('recommended_frames', [])),
            ai_reason=data.get('ai_reason'),
            selected_frame=data.get('selected_frame')
        )
        db.session.add(rec)
        db.session.commit()
        return jsonify({"message": "Recommendation saved successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@recommendation_bp.route('/history/<int:customer_id>', methods=['GET'])
@roles_required('admin', 'staff')
def get_history(customer_id):
    history = FrameRecommendation.query.filter_by(customer_id=customer_id).order_by(FrameRecommendation.created_at.desc()).all()
    return jsonify([h.to_dict() for h in history]), 200
