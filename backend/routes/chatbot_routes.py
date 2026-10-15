from flask import Blueprint, request, jsonify
from auth_utils import roles_required
from flask_jwt_extended import get_jwt_identity
from models import db, ChatHistory, User
from utils.ai_chat import generate_chat_response

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/message', methods=['POST'])
@roles_required('admin', 'staff')
def chat_message():
    data = request.get_json()
    message = data.get('message')
    customer_id = data.get('customer_id') # Optional
    
    if not message or not message.strip():
        return jsonify({"message": "Message cannot be empty."}), 400
        
    current_user_id = get_jwt_identity()
    
    try:
        # Get AI Response
        ai_response = generate_chat_response(message)
        
        # Save to database
        chat_log = ChatHistory(
            user_id=current_user_id,
            customer_id=customer_id if customer_id else None,
            question=message,
            answer=ai_response
        )
        db.session.add(chat_log)
        db.session.commit()
        
        return jsonify({"answer": ai_response}), 200
        
    except Exception as e:
        db.session.rollback()
        print("Chatbot Route Error:", e)
        return jsonify({"message": "I'm sorry, I encountered an internal error processing your request."}), 500


@chatbot_bp.route('/history', methods=['GET'])
@roles_required('admin')
def get_chat_history():
    history = ChatHistory.query.order_by(ChatHistory.created_at.desc()).limit(100).all()
    return jsonify([h.to_dict() for h in history]), 200
