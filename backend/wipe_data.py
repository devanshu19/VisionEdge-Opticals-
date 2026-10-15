from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    print("Dropping all existing tables to remove all data...")
    db.drop_all()
    
    print("Recreating empty tables...")
    db.create_all()
    
    print("Recreating admin user...")
    admin = User(
        username='admin', 
        password_hash=generate_password_hash('admin123'), 
        email='admin@visionedge.com', 
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()
    print("Done! Database is now empty and ready for new data.")
