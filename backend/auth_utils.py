from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models import User

def roles_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user_id = None
            try:
                verify_jwt_in_request(optional=True)
                current_user_id = get_jwt_identity()
            except Exception:
                pass
                
            if current_user_id:
                try:
                    user = User.query.get(int(current_user_id))
                except (ValueError, TypeError):
                    user = None

                if user:
                    user_role = (user.role or '').strip().lower()
                    allowed_lower = [r.strip().lower() for r in allowed_roles]
                    if user_role in allowed_lower or 'guest' in allowed_lower:
                        return fn(*args, **kwargs)
                    else:
                        return jsonify({"message": "You do not have permission to access this resource."}), 403

            if 'guest' in [r.strip().lower() for r in allowed_roles]:
                return fn(*args, **kwargs)

            return jsonify({"message": "Authentication required"}), 401
        return wrapper
    return decorator
