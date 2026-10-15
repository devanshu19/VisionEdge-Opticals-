import os
import sys

# Add backend directory to sys.path
backend_dir = r'c:\projects\VisionEdge\backend'
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app import create_app
from models import db, User

app = create_app()
app.config['TESTING'] = True
app.config['DEBUG'] = True

def test_endpoints():
    print("=== Testing VisionEdge AI Endpoints ===")
    with app.test_client() as client:
        with app.app_context():
            # Get or create a test user
            user = User.query.filter_by(role='customer').first()
            if not user:
                user = User.query.first()
            
            user_id = user.id if user else 1
            
            from flask_jwt_extended import create_access_token
            access_token = create_access_token(identity=str(user_id))
            headers = {'Authorization': f'Bearer {access_token}'}

            # 1. Test VTO Frames endpoint
            print("\n1. Testing GET /api/vto/frames ...")
            res = client.get('/api/vto/frames', headers=headers, follow_redirects=True)
            print("Status Code:", res.status_code)
            if res.status_code == 200:
                data = res.get_json()
                print("Frames Returned:", len(data))
                if len(data) > 0:
                    print("Sample Frame:", data[0].get('name'), "| VTO Image:", data[0].get('vto_image'))

            # 2. Test Frame Recommendation Generate endpoint
            print("\n2. Testing POST /api/recommendations/generate ...")
            res = client.post('/api/recommendations/generate', headers=headers, json={"face_shape": "Oval"}, follow_redirects=True)
            print("Status Code:", res.status_code)
            if res.status_code == 200:
                data = res.get_json()
                print("Success Message:", data.get('message'))
                print("Recommended Frames Count:", len(data.get('recommendations', [])))

            # 3. Test Lens Recommendation Save endpoint
            print("\n3. Testing POST /api/lens-recommendations/save ...")
            res = client.post('/api/lens-recommendations/save', headers=headers, json={
                "recommended_lens": "1.67 High-Index Thin Lens",
                "reason": "-3.50 SPH diopter high power requirement"
            }, follow_redirects=True)
            print("Status Code:", res.status_code)
            if res.status_code in [200, 201]:
                print("Response JSON:", res.get_json())

            # 4. Test AI Prescription OCR extraction endpoint
            print("\n4. Testing POST /api/ai/extract ...")
            import io
            dummy_file = (io.BytesIO(b"fake image content"), 'prescription.jpg')
            res = client.post('/api/ai/extract', headers=headers, data={'file': dummy_file}, content_type='multipart/form-data')
            print("Status Code:", res.status_code)
            if res.status_code == 200:
                print("Extracted Data JSON:", res.get_json().get('data'))

    print("\n=== AI Endpoints Test Execution Finished Successfully ===")

if __name__ == '__main__':
    test_endpoints()
