from flask import Blueprint, request, jsonify
from auth_utils import roles_required
from models import db, LensRecommendation
import json

lens_rec_bp = Blueprint('lens_recommendation', __name__)

@lens_rec_bp.route('/save', methods=['POST'])
@roles_required('admin', 'staff', 'customer', 'guest')
def save_lens_recommendation():
    data = request.get_json() or {}
    
    customer_id = data.get('customer_id')
    if not customer_id:
        # Return generated recommendation payload even if guest/not logged in
        return jsonify({
            "message": "Lens recommendation generated",
            "recommended_lens": data.get('recommended_lens', 'Single Vision 1.56 Blue-Cut'),
            "reason": data.get('reason', 'Based on user input diopters and lifestyle profile')
        }), 200
        
    try:
        rec = LensRecommendation(
            customer_id=customer_id,
            prescription_id=data.get('prescription_id'),
            recommended_lens=data.get('recommended_lens'),
            reason=data.get('reason'),
            ai_response=json.dumps(data.get('ai_response', {})) if isinstance(data.get('ai_response'), dict) else data.get('ai_response')
        )
        db.session.add(rec)
        db.session.commit()
        return jsonify({"message": "Lens recommendation saved successfully", "id": rec.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@lens_rec_bp.route('/history/<int:customer_id>', methods=['GET'])
@roles_required('admin', 'staff', 'customer')
def get_history(customer_id):
    history = LensRecommendation.query.filter_by(customer_id=customer_id).order_by(LensRecommendation.created_at.desc()).all()
    result = []
    for h in history:
        result.append({
            "id": h.id,
            "customer_id": h.customer_id,
            "prescription_id": h.prescription_id,
            "recommended_lens": h.recommended_lens,
            "reason": h.reason,
            "ai_response": h.ai_response,
            "created_at": str(h.created_at)
        })
    return jsonify(result), 200
