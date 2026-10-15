from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    # Check if admin exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@visionedge.com',
            password_hash=generate_password_hash('password123'),
            role='admin',
            first_name='Admin',
            last_name='User'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully.")
    else:
        admin.password_hash = generate_password_hash('password123')
        db.session.commit()
        print("Admin user password reset to password123.")
