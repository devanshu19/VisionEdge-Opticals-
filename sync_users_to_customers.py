import os
import sqlite3
import pymysql
from dotenv import load_dotenv

load_dotenv('backend/.env')

def sync_db():
    print("--- SYNCING USERS TO CUSTOMERS ---")
    
    # 1. Sync SQLite Database
    sqlite_path = r'backend/visionedge.db'
    if os.path.exists(sqlite_path):
        conn = sqlite3.connect(sqlite_path)
        cur = conn.cursor()
        users = cur.execute("SELECT id, username, email, phone, role FROM user WHERE role='customer'").fetchall()
        for u in users:
            uid, uname, email, phone, role = u
            parts = uname.split('.')
            fname = parts[0].capitalize() if parts else 'Customer'
            lname = parts[1].capitalize() if len(parts) > 1 else ''
            
            existing = cur.execute("SELECT id FROM customer WHERE email=?", (email,)).fetchone()
            if not existing:
                cur.execute("SELECT MAX(id) FROM customer")
                max_id = cur.fetchone()[0] or 0
                next_id = max_id + 1
                code = f"CUST{next_id:04d}"
                cur.execute("""
                    INSERT INTO customer (id, customer_code, first_name, last_name, email, phone, status, created_at, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, 'Active', DATETIME('now'), ?)
                """, (next_id, code, fname, lname, email, phone or '', uid))
                cur.execute("""
                    INSERT INTO customer_profile (customer_id, blood_group, eye_conditions, allergies, notes)
                    VALUES (?, '', '', '', '')
                """, (next_id,))
                print(f"[SQLite] Synced user '{uname}' ({email}) -> Customer Code '{code}'")
        conn.commit()
        conn.close()

    # 2. Sync MySQL Database
    try:
        mconn = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '3306')),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'visionedge_db')
        )
        mcur = mconn.cursor()

        # Add purav chaudhari & arpit mistry if missing in MySQL
        mcur.execute("SELECT id, username, email FROM user WHERE email IN ('purav1912@gmail.com', 'arpit12@gmail.com')")
        users_in_mysql = {row[2]: row for row in mcur.fetchall()}

        target_users = [
            ("purav.chaudhari", "Purav", "Chaudhari", "purav1912@gmail.com", "customer"),
            ("arpit.mistry", "Arpit", "Mistry", "arpit12@gmail.com", "customer")
        ]

        for uname, fname, lname, email, role in target_users:
            # Check user
            mcur.execute("SELECT id FROM user WHERE email=%s", (email,))
            u_row = mcur.fetchone()
            if not u_row:
                mcur.execute("SELECT MAX(id) FROM user")
                max_uid = (mcur.fetchone()[0] or 0) + 1
                # Insert default password hash
                from werkzeug.security import generate_password_hash
                pw_hash = generate_password_hash("password123")
                mcur.execute("""
                    INSERT INTO user (id, username, first_name, last_name, email, phone, password_hash, role, created_at)
                    VALUES (%s, %s, %s, %s, %s, '9876543210', %s, 'customer', NOW())
                """, (max_uid, uname, fname, lname, email, pw_hash))
                uid = max_uid
            else:
                uid = u_row[0]

            # Check customer
            mcur.execute("SELECT id FROM customer WHERE email=%s", (email,))
            c_row = mcur.fetchone()
            if not c_row:
                mcur.execute("SELECT MAX(id) FROM customer")
                max_cid = (mcur.fetchone()[0] or 0) + 1
                code = f"CUST{max_cid:04d}"
                mcur.execute("""
                    INSERT INTO customer (id, customer_code, first_name, last_name, email, phone, status, created_at, created_by)
                    VALUES (%s, %s, %s, %s, %s, '9876543210', 'Active', NOW(), %s)
                """, (max_cid, code, fname, lname, email, uid))
                mcur.execute("""
                    INSERT INTO customer_profile (customer_id) VALUES (%s)
                """, (max_cid,))
                print(f"[MySQL] Synced customer '{fname} {lname}' ({email}) -> Code '{code}'")

        mconn.commit()
        mconn.close()
    except Exception as e:
        print("MySQL sync error:", e)

if __name__ == '__main__':
    sync_db()
