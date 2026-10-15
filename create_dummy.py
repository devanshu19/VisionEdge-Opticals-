import requests
import time

def add_dummy():
    # Login as admin to get token
    login = requests.post("http://localhost:5000/api/auth/login", json={"username": "admin", "password": "password123"})
    token = login.json().get('access_token')
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create customer
    data = {
        "first_name": "Arjun",
        "last_name": "Sharma",
        "gender": "Male",
        "dob": "1985-06-15",
        "occupation": "Software Engineer",
        "phone": "9876543210",
        "email": "arjun.s@example.com",
        "address": "123 Tech Park, Sector 4",
        "city": "Bengaluru",
        "state": "Karnataka",
        "pincode": "560001",
        "eye_condition": "Mild astigmatism in left eye",
        "lens_preference": "Anti-glare, Blue Cut",
        "frame_preference": "Rectangular, Titanium"
    }
    
    res = requests.post("http://localhost:5000/api/customers/", json=data, headers=headers)
    print("Create:", res.json())

if __name__ == '__main__':
    add_dummy()
