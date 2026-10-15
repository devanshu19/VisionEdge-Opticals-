import requests
import sqlite3

# Make sure we have a staff user
def setup_db():
    conn = sqlite3.connect('C:/projects/VisionEdge/backend/instance/visionedge.db')
    c = conn.cursor()
    try:
        from werkzeug.security import generate_password_hash
        pw = generate_password_hash('password123')
        c.execute("INSERT OR IGNORE INTO user (username, password_hash, role) VALUES ('staff1', ?, 'staff')", (pw,))
        conn.commit()
    except Exception as e:
        print("DB error:", e)
    finally:
        conn.close()

def test_api():
    base_url = "http://localhost:5000/api"
    
    print("--- Testing API Restrictions ---")
    
    # 1. Test unauthenticated request
    r = requests.get(f"{base_url}/customers/")
    print(f"Unauthenticated /customers: {r.status_code}")
    
    # 2. Login as admin
    r = requests.post(f"{base_url}/auth/login", json={"username": "admin", "password": "password123"})
    if r.status_code == 200:
        admin_token = r.json().get('access_token')
        print(f"Admin login successful")
        
        # Admin testing inventory
        r = requests.get(f"{base_url}/inventory/", headers={"Authorization": f"Bearer {admin_token}"})
        print(f"Admin /inventory/: {r.status_code}")
    else:
        print("Admin login failed", r.text)
        
    # 3. Login as staff
    r = requests.post(f"{base_url}/auth/login", json={"username": "staff1", "password": "password123"})
    if r.status_code == 200:
        staff_token = r.json().get('access_token')
        print(f"Staff login successful")
        
        # Staff testing customers (should be allowed)
        r = requests.get(f"{base_url}/customers/", headers={"Authorization": f"Bearer {staff_token}"})
        print(f"Staff /customers/: {r.status_code}")
        
        # Staff testing inventory (should be forbidden)
        r = requests.get(f"{base_url}/inventory/", headers={"Authorization": f"Bearer {staff_token}"})
        print(f"Staff /inventory/: {r.status_code} (Expected 403)")
        if r.status_code == 403:
            print("RBAC works properly!")
    else:
        print("Staff login failed", r.text)

if __name__ == '__main__':
    setup_db()
    test_api()
