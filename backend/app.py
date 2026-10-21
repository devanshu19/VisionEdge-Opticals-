from flask import Flask, jsonify, request
from config import Config
from models import db
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ------------------------------------------------------------------ #
    # Log the active database dialect at startup (without exposing secrets)
    # ------------------------------------------------------------------ #
    import sys
    dialect = Config.db_dialect()
    print(f"[VisionEdge] Database dialect: {dialect} (Target: Supabase PostgreSQL)", file=sys.stdout, flush=True)

    # Initialize extensions
    from flask_cors import CORS
    default_origins = [
        "https://visionopticals.netlify.app",
        "http://localhost:8000",
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ]
    configured_origins = [o for o in (Config.FRONTEND_URL, *Config.CORS_ALLOWED_ORIGINS) if o]
    cors_origins = list(dict.fromkeys((*configured_origins, *default_origins)))
    CORS(
        app,
        resources={r"/*": {"origins": cors_origins}},
        supports_credentials=True,
    )
    db.init_app(app)
    jwt = JWTManager(app)

    # WhiteNoise Static File Serving
    from whitenoise import WhiteNoise
    import os
    static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    os.makedirs(static_folder, exist_ok=True)
    app.wsgi_app = WhiteNoise(app.wsgi_app, root=static_folder, prefix="static/")

    # Security Headers (force_https disabled for local HTTP development)
    from flask_talisman import Talisman
    Talisman(app, force_https=False, content_security_policy=None)

    # Setup Logging
    import logging
    from logging.handlers import RotatingFileHandler

    os.makedirs("logs", exist_ok=True)
    handler = RotatingFileHandler("logs/application.log", maxBytes=100_000, backupCount=3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("VisionEdge backend initialized. DB dialect: %s", dialect)

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.customer_routes import customer_bp
    from routes.prescription_routes import prescription_bp
    from routes.inventory_routes import inventory_bp
    from routes.billing_routes import billing_bp
    from routes.order_routes import order_bp
    from routes.reports_routes import reports_bp
    from routes.ai_routes import ai_bp
    from routes.frame_recommendation_routes import recommendation_bp
    from routes.lens_recommendation_routes import lens_rec_bp
    from routes.virtual_tryon_routes import vto_bp
    from routes.chatbot_routes import chatbot_bp
    from routes.notification_routes import notification_bp
    from routes.appointment_routes import appointment_bp
    from routes.payment_routes import payment_bp
    from routes.razorpay_routes import razorpay_bp
    from utils.signals import register_signals

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(customer_bp, url_prefix="/api/customers")
    app.register_blueprint(customer_bp, url_prefix="/api/customer", name="customer_singular")
    app.register_blueprint(prescription_bp, url_prefix="/api/prescriptions")
    app.register_blueprint(prescription_bp, url_prefix="/api/prescription", name="prescription_singular")
    app.register_blueprint(inventory_bp, url_prefix="/api/inventory")
    app.register_blueprint(billing_bp, url_prefix="/api/billing")
    app.register_blueprint(order_bp, url_prefix="/api/orders")
    app.register_blueprint(reports_bp, url_prefix="/api/reports")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")
    app.register_blueprint(recommendation_bp, url_prefix="/api/recommendations")
    app.register_blueprint(lens_rec_bp, url_prefix="/api/lens-recommendations")
    app.register_blueprint(vto_bp, url_prefix="/api/vto")
    app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")
    app.register_blueprint(notification_bp, url_prefix="/api/notifications")
    app.register_blueprint(appointment_bp, url_prefix="/api/appointments")
    app.register_blueprint(payment_bp, url_prefix="/api/payment")
    app.register_blueprint(razorpay_bp, url_prefix="/api/payment/razorpay")

    # Register SQLAlchemy event listeners
    with app.app_context():
        register_signals()

    # Flask-Admin Setup
    try:
        from flask_admin import Admin
        from flask_admin.contrib.sqla import ModelView
        admin = Admin(app, name="VisionEdge Admin")
        from models import User, Customer, Frame, Lens, Order, Billing, Appointment
        admin.add_view(ModelView(User, db.session, endpoint="admin_user"))
        admin.add_view(ModelView(Customer, db.session, endpoint="admin_customer"))
        admin.add_view(ModelView(Frame, db.session, endpoint="admin_frame"))
        admin.add_view(ModelView(Lens, db.session, endpoint="admin_lens"))
        admin.add_view(ModelView(Order, db.session, endpoint="admin_order"))
        admin.add_view(ModelView(Billing, db.session, endpoint="admin_billing"))
        admin.add_view(ModelView(Appointment, db.session, endpoint="admin_appointment"))
    except ImportError:
        print("Flask-Admin not installed. Skipping admin panel setup.")

    @app.route("/", methods=["GET"])
    @app.route("/api", methods=["GET"])
    @app.route("/api/health", methods=["GET"])
    def health_check():
        from sqlalchemy import text
        db_status = "disconnected"
        db_dialect_info = dialect
        try:
            result = db.session.execute(text("SELECT 1"))
            result.close()
            db_status = "connected"
        except Exception as e:
            app.logger.error("Health check DB error: %s", type(e).__name__)

        status_code = 200 if db_status == "connected" else 503
        return jsonify({
            "status": "healthy" if db_status == "connected" else "degraded",
            "database": db_status,
            "dialect": db_dialect_info,
            "message": "VisionEdge API is running",
        }), status_code

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.error("404 Error: %s", request.url)
        return jsonify({"message": "Resource not found. Please contact administrator if this persists."}), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        app.logger.warning("403 Forbidden: %s", request.url)
        return jsonify({"message": "You don't have permission to perform this action."}), 403

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error("500 Server Error: %s", error)
        db.session.rollback()
        return jsonify({"message": "Something went wrong on the server. Please contact administrator."}), 500

    import os
    from flask import send_from_directory

    @app.route("/media/<path:filename>")
    @app.route("/api/media/<path:filename>")
    def serve_media(filename):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return send_from_directory(os.path.join(base_dir, "media"), filename)

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        try:
            db.create_all()
            print("Successfully connected to the database and created tables.")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            print("Please check your DATABASE_URL configuration.")

    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])
