"""
VisionEdge — Simple Authentication System Test Suite
===================================================
Tests all aspects of the simplified Email + Password authentication system:
- Registration (signup)
- Validation & hashing
- Role security (customer only)
- Login (email & username)
- Invalid credentials & error handling
- Token issuance & session persistence (/me)
- One-click logout
- Role-based authorization & admin access protection
- Health check
"""

import os
import sys
import unittest
import json
from datetime import datetime
from werkzeug.security import generate_password_hash

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Ensure test configuration
os.environ["USE_SQLITE"] = "true"
os.environ["APP_ENV"] = "development"

from app import create_app
from models import db, User, Customer, CustomerProfile

class SimpleAuthTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()

            # Create or ensure an admin user exists
            admin = User.query.filter_by(username="admin_test").first()
            if not admin:
                admin = User(
                    username="admin_test",
                    email="admin_test@visionedge.com",
                    first_name="Admin",
                    last_name="Test",
                    password_hash=generate_password_hash("AdminPass123!"),
                    role="admin"
                )
                db.session.add(admin)
                db.session.commit()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            # Clean up test customers and profiles
            test_custs = Customer.query.filter(Customer.email.like("%@test-visionedge.com")).all()
            for tc in test_custs:
                if tc.profile:
                    db.session.delete(tc.profile)
                db.session.delete(tc)
            # Clean up test users
            User.query.filter(User.email.like("%@test-visionedge.com")).delete(synchronize_session=False)
            User.query.filter_by(username="admin_test").delete()
            db.session.commit()

    def test_01_customer_registration_success(self):
        """Test successful registration with full name, email, password."""
        res = self.client.post("/api/auth/register", json={
            "full_name": "Test Customer",
            "email": "cust1@test-visionedge.com",
            "password": "Password123!"
        })
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data.get("access_token"))
        self.assertIn("user", data)
        self.assertEqual(data["user"]["email"], "cust1@test-visionedge.com")
        self.assertEqual(data["user"]["role"], "customer")

        # Verify DB records
        with self.app.app_context():
            u = User.query.filter_by(email="cust1@test-visionedge.com").first()
            self.assertIsNotNone(u)
            self.assertEqual(u.first_name, "Test")
            self.assertEqual(u.last_name, "Customer")
            # Verify Customer model created
            c = Customer.query.filter_by(email="cust1@test-visionedge.com").first()
            self.assertIsNotNone(c)
            self.assertIsNotNone(c.profile)

    def test_02_registration_duplicate_email(self):
        """Test that registering with an existing email is rejected."""
        res = self.client.post("/api/auth/register", json={
            "full_name": "Duplicate User",
            "email": "cust1@test-visionedge.com",
            "password": "Password123!"
        })
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertIn("already exists", data.get("message", "").lower())

    def test_03_registration_short_password(self):
        """Test that passwords shorter than 6 characters are rejected."""
        res = self.client.post("/api/auth/register", json={
            "full_name": "Short Pwd",
            "email": "short@test-visionedge.com",
            "password": "123"
        })
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertIn("at least 6 characters", data.get("message", "").lower())

    def test_04_registration_invalid_email(self):
        """Test that invalid email format is rejected."""
        res = self.client.post("/api/auth/register", json={
            "full_name": "Bad Email",
            "email": "not-an-email",
            "password": "Password123!"
        })
        self.assertEqual(res.status_code, 400)

    def test_05_registration_role_tampering_prevented(self):
        """Test that public registration cannot grant admin role."""
        res = self.client.post("/api/auth/register", json={
            "full_name": "Hacker Attempt",
            "email": "hacker@test-visionedge.com",
            "password": "Password123!",
            "role": "admin"  # Tamper attempt
        })
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertEqual(data["user"]["role"], "customer")

    def test_06_customer_login_success(self):
        """Test customer login with email and password."""
        res = self.client.post("/api/auth/login", json={
            "email": "cust1@test-visionedge.com",
            "password": "Password123!"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("access_token"))
        self.assertEqual(data["user"]["email"], "cust1@test-visionedge.com")
        self.assertEqual(data.get("redirect_url"), "/dashboard.html")

    def test_07_customer_login_case_insensitive_email(self):
        """Test that login email is case-insensitive."""
        res = self.client.post("/api/auth/login", json={
            "email": "CUST1@TEST-VISIONEDGE.COM",
            "password": "Password123!"
        })
        self.assertEqual(res.status_code, 200)

    def test_08_login_with_username(self):
        """Test login using username instead of email."""
        with self.app.app_context():
            u = User.query.filter_by(email="cust1@test-visionedge.com").first()
            username = u.username

        res = self.client.post("/api/auth/login", json={
            "username": username,
            "password": "Password123!"
        })
        self.assertEqual(res.status_code, 200)

    def test_09_login_incorrect_password(self):
        """Test login failure with wrong password."""
        res = self.client.post("/api/auth/login", json={
            "email": "cust1@test-visionedge.com",
            "password": "WrongPassword!"
        })
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertIn("invalid", data.get("message", "").lower())

    def test_10_login_nonexistent_user(self):
        """Test login failure with nonexistent email."""
        res = self.client.post("/api/auth/login", json={
            "email": "nobody@test-visionedge.com",
            "password": "Password123!"
        })
        self.assertEqual(res.status_code, 401)

    def test_11_login_empty_fields(self):
        """Test login with empty fields returns 400."""
        res = self.client.post("/api/auth/login", json={})
        self.assertEqual(res.status_code, 400)

    def test_12_logout_endpoint(self):
        """Test one-click logout endpoint returns 200."""
        res = self.client.post("/api/auth/logout")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("logged out", data.get("message", "").lower())

    def test_13_current_user_me_endpoint(self):
        """Test /api/auth/me returns current user profile with valid JWT."""
        login_res = self.client.post("/api/auth/login", json={
            "email": "cust1@test-visionedge.com",
            "password": "Password123!"
        })
        token = login_res.get_json()["access_token"]

        res = self.client.get("/api/auth/me", headers={
            "Authorization": f"Bearer {token}"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["email"], "cust1@test-visionedge.com")
        self.assertEqual(data["role"], "customer")
        self.assertTrue("customer_id" in data)

    def test_14_current_user_unauthorized(self):
        """Test /api/auth/me without token returns 401."""
        res = self.client.get("/api/auth/me")
        self.assertEqual(res.status_code, 401)

    def test_15_admin_login(self):
        """Test admin login returns redirect to admin panel."""
        res = self.client.post("/api/auth/login", json={
            "username": "admin_test",
            "password": "AdminPass123!"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["user"]["role"], "admin")
        self.assertEqual(data.get("redirect_url"), "/admin/index.html")

    def test_16_customer_blocked_from_admin_api(self):
        """Test that a customer token cannot access admin-only endpoints."""
        login_res = self.client.post("/api/auth/login", json={
            "email": "cust1@test-visionedge.com",
            "password": "Password123!"
        })
        token = login_res.get_json()["access_token"]

        # /api/auth/users is admin-only
        res = self.client.get("/api/auth/users", headers={
            "Authorization": f"Bearer {token}"
        })
        self.assertEqual(res.status_code, 403)

    def test_17_admin_accesses_admin_api(self):
        """Test that an admin token successfully accesses admin-only endpoints."""
        login_res = self.client.post("/api/auth/login", json={
            "username": "admin_test",
            "password": "AdminPass123!"
        })
        token = login_res.get_json()["access_token"]

        res = self.client.get("/api/auth/users", headers={
            "Authorization": f"Bearer {token}"
        })
        self.assertEqual(res.status_code, 200)

    def test_18_health_check_endpoint(self):
        """Test /api/health endpoint reports database connectivity."""
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get("status"), "healthy")
        self.assertEqual(data.get("database"), "connected")

    def test_19_change_password(self):
        """Test password change workflow."""
        login_res = self.client.post("/api/auth/login", json={
            "email": "cust1@test-visionedge.com",
            "password": "Password123!"
        })
        token = login_res.get_json()["access_token"]

        # Change to new password
        res = self.client.post("/api/auth/change-password", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "current_password": "Password123!",
            "new_password": "NewSecretPassword456!"
        })
        self.assertEqual(res.status_code, 200)

        # Login with old password should fail
        res_old = self.client.post("/api/auth/login", json={
            "email": "cust1@test-visionedge.com",
            "password": "Password123!"
        })
        self.assertEqual(res_old.status_code, 401)

        # Login with new password should succeed
        res_new = self.client.post("/api/auth/login", json={
            "email": "cust1@test-visionedge.com",
            "password": "NewSecretPassword456!"
        })
        self.assertEqual(res_new.status_code, 200)

if __name__ == "__main__":
    unittest.main()
