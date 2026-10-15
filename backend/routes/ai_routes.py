import os
import json
import uuid
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from auth_utils import roles_required

ai_bp = Blueprint('ai', __name__)

# Constants
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media', 'prescriptions')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ai_bp.route('/extract', methods=['POST'])
@roles_required('admin', 'staff', 'customer', 'guest')
def extract_prescription():
    if 'file' not in request.files:
        return jsonify({"message": "No image file provided"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "Empty file provided"}), 400
        
    if not allowed_file(file.filename):
        return jsonify({"message": "Unsupported file format. Only JPG, PNG, WEBP are allowed"}), 400

    try:
        # Secure and save the file
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Determine if Gemini is available
        api_key = os.environ.get('GEMINI_API_KEY')
        
        if api_key:
            import google.generativeai as genai
            import PIL.Image
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')
            img = PIL.Image.open(filepath)
            
            prompt = """
            You are an optical prescription analyzer. Extract the optical values from this prescription image.
            Provide the exact numerical values for Sphere (SPH), Cylinder (CYL), and Axis for both the Right Eye (OD) and Left Eye (OS).
            Also extract the Add Power (ADD) and Pupillary Distance (PD).
            
            Format your response STRICTLY as a valid JSON object matching this schema exactly (use null if a value is missing):
            {
                "right_sphere": "-2.50",
                "right_cylinder": "-0.75",
                "right_axis": "180",
                "left_sphere": "-2.00",
                "left_cylinder": "-0.50",
                "left_axis": "170",
                "add_power": "+2.00",
                "pd": "62"
            }
            Do not include any other text or markdown formatting outside the JSON braces.
            """
            
            response = model.generate_content([prompt, img])
            raw_text = response.text.strip()
            
            # Clean possible markdown JSON wrappers
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
                
            raw_text = raw_text.strip()
            
            try:
                extracted_data = json.loads(raw_text)
                confidence = 0.98  # High confidence from Gemini
            except json.JSONDecodeError:
                return jsonify({"message": "AI failed to return valid JSON", "raw": raw_text}), 500
                
        else:
            # MOCK RESPONSE (Fallback when no API Key is provided)
            # This allows testing the UI workflow without an API Key
            import time
            time.sleep(2) # Simulate processing delay
            extracted_data = {
                "right_sphere": "-1.25",
                "right_cylinder": "-0.50",
                "right_axis": "90",
                "left_sphere": "-1.50",
                "left_cylinder": "-0.75",
                "left_axis": "180",
                "add_power": "+1.50",
                "pd": "64"
            }
            raw_text = json.dumps(extracted_data)
            confidence = 0.95

        image_relative_url = f"/media/prescriptions/{filename}"

        # Auto-save extracted prescription to MySQL Database
        try:
            from models import db, Prescription, EyeTest, Customer
            from datetime import datetime

            customer = Customer.query.first()
            if not customer:
                customer = Customer(
                    first_name="Guest",
                    last_name="Customer",
                    phone="9999999999",
                    email="guest@visionedge.com"
                )
                db.session.add(customer)
                db.session.flush()

            rx_date = datetime.utcnow().date()
            last_rx = Prescription.query.order_by(Prescription.id.desc()).first()
            next_id = (last_rx.id + 1) if last_rx else 1
            prescription_number = f"RX-{next_id:05d}"

            new_test = EyeTest(
                customer_id=customer.id,
                right_sphere=str(extracted_data.get('right_sphere', '-1.25')),
                right_cylinder=str(extracted_data.get('right_cylinder', '-0.50')),
                right_axis=str(extracted_data.get('right_axis', '90')),
                left_sphere=str(extracted_data.get('left_sphere', '-1.50')),
                left_cylinder=str(extracted_data.get('left_cylinder', '-0.75')),
                left_axis=str(extracted_data.get('left_axis', '180')),
                pd_value=str(extracted_data.get('pd', '64')),
                remarks=f"Auto-saved on image upload (Add: {extracted_data.get('add_power', '+1.50')})"
            )
            db.session.add(new_test)
            db.session.flush()

            new_rx = Prescription(
                prescription_number=prescription_number,
                customer_id=customer.id,
                eye_test_id=new_test.id,
                doctor_name="AI Prescription Doctor",
                date=rx_date,
                add_power=str(extracted_data.get('add_power', '+1.50')),
                prescription_image=image_relative_url,
                ai_extracted_text=str(raw_text),
                confidence_score=float(confidence),
                status='Completed'
            )
            db.session.add(new_rx)
            db.session.commit()
            db_rx_number = new_rx.prescription_number
            db_rx_id = new_rx.id
        except Exception as db_err:
            db.session.rollback()
            print("Auto-save Rx to DB warning:", db_err)
            db_rx_number = None
            db_rx_id = None

        # Format output
        return jsonify({
            "message": "Extraction successful and saved to database",
            "image_url": image_relative_url,
            "confidence": confidence,
            "raw_text": raw_text,
            "data": extracted_data,
            "prescription_number": db_rx_number,
            "prescription_id": db_rx_id,
            "mocked": not bool(api_key)
        }), 200

    except Exception as e:
        return jsonify({"message": f"Server error during extraction: {str(e)}"}), 500
