from flask import Blueprint, request, jsonify, current_app
from auth_utils import roles_required
from models import db, Frame, Customer, VirtualTryOnHistory
import os
import uuid
import base64

vto_bp = Blueprint('vto', __name__)

@vto_bp.route('/frames', methods=['GET'])
@roles_required('admin', 'staff', 'customer', 'guest')
def get_vto_frames():
    # Only return frames that have a vto_image set and are in stock
    # For demonstration, if no frames have vto_image set, we will return ALL frames
    # and just mock the vto_image to a generic transparent frame URL so the UI works.
    
    frames = Frame.query.filter(Frame.stock > 0).all()
    
    vto_ready_frames = []
    for f in frames:
        brand_name = f.brand if (isinstance(f.brand, str) and f.brand) else (getattr(f.brand, 'name', None) or "Unknown")
        
        # If no explicit vto_image, use a placeholder transparent frame
        vto_img = f.vto_image if f.vto_image else "/api/media/frames/rayban_vto.png"
        
        vto_ready_frames.append({
            "id": f.id,
            "name": f.name,
            "brand": brand_name,
            "shape": f.shape,
            "price": f.selling_price,
            "image": f.image,
            "vto_image": vto_img
        })
        
    return jsonify(vto_ready_frames), 200


@vto_bp.route('/save-history', methods=['POST'])
@roles_required('admin', 'staff', 'customer', 'guest')
def save_vto_history():
    data = request.get_json() or {}
    
    customer_id = data.get('customer_id')
    if not customer_id:
        cust = Customer.query.first()
        customer_id = cust.id if cust else 1

    frame_id = data.get('frame_id')
    frame = Frame.query.get(frame_id) if frame_id else None
    if not frame:
        frame = Frame.query.first()
    frame_id = frame.id if frame else None
    snapshot_base64 = data.get('snapshot') # data:image/jpeg;base64,...
    
    if not snapshot_base64:
        return jsonify({"message": "Missing snapshot base64 image data"}), 400
        
    # Save the base64 snapshot as a file
    try:
        header, encoded = snapshot_base64.split(",", 1)
        file_ext = "jpg" if "jpeg" in header else "png"
        
        filename = f"vto_{uuid.uuid4().hex}.{file_ext}"
        save_dir = os.path.join(current_app.root_path, 'media', 'vto_history')
        os.makedirs(save_dir, exist_ok=True)
        
        filepath = os.path.join(save_dir, filename)
        
        with open(filepath, "wb") as f:
            f.write(base64.b64decode(encoded))
            
        image_url = f"/api/media/vto_history/{filename}"
        
        # Save to database
        history = VirtualTryOnHistory(
            customer_id=customer_id,
            frame_id=frame_id,
            tryon_image=image_url
        )
        db.session.add(history)
        db.session.commit()
        
        return jsonify({"message": "Saved successfully", "history_id": history.id}), 201
        
    except Exception as e:
        db.session.rollback()
        print("VTO Save Error:", e)
        return jsonify({"message": str(e)}), 500


@vto_bp.route('/history/<int:customer_id>', methods=['GET'])
@roles_required('admin', 'staff', 'customer')
def get_customer_vto_history(customer_id):
    history = VirtualTryOnHistory.query.filter_by(customer_id=customer_id).order_by(VirtualTryOnHistory.created_at.desc()).all()
    return jsonify([h.to_dict() for h in history]), 200
