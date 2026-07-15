from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db
from flask_jwt_extended import JWTManager
import pymysql

pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app) # Allow frontend to communicate with backend
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.customer_routes import customer_bp
    from routes.prescription_routes import prescription_bp
    from routes.inventory_routes import inventory_bp
    from routes.billing_routes import billing_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(customer_bp, url_prefix='/api/customers')
    app.register_blueprint(prescription_bp, url_prefix='/api/prescriptions')
    app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
    app.register_blueprint(billing_bp, url_prefix='/api/billing')
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "message": "VisionEdge Backend API is running."}), 200
        
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        try:
            db.create_all()
            print("Successfully connected to MySQL and created tables.")
        except Exception as e:
            print(f"Error connecting to MySQL: {e}")
            print("Please ensure MySQL is running and the 'visionedge' database exists.")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
