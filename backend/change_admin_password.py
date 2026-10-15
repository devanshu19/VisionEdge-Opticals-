from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash
import sys


def change_password(username: str, new_password: str):
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"User '{username}' not found.")
            return 1
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        print(f"Password for user '{username}' updated successfully.")
        return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python change_admin_password.py <new_password> [username]")
        sys.exit(1)
    new_pw = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else 'admin'
    exit_code = change_password(username, new_pw)
    sys.exit(exit_code)
