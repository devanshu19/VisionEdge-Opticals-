import sqlite3
import pymysql
import os
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

load_dotenv('backend/.env')

pw = generate_password_hash("password123")

print("--- SQLITE ADMIN RESET ---")
conn = sqlite3.connect('backend/visionedge.db')
cur = conn.cursor()
cur.execute("UPDATE user SET password_hash = ? WHERE username = 'admin' OR email = 'admin@visionedge.com'", (pw,))
conn.commit()
for r in cur.execute("SELECT id, username, email, role FROM user WHERE role='admin'"):
    print(" ", r)
conn.close()

print("--- MYSQL ADMIN RESET ---")
mconn = pymysql.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', '3306')),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'visionedge_db')
)
mcur = mconn.cursor()
mcur.execute("UPDATE user SET password_hash = %s WHERE username = 'admin' OR email = 'admin@visionedge.com'", (pw,))
mconn.commit()
mcur.execute("SELECT id, username, email, role FROM user WHERE role='admin'")
for r in mcur.fetchall():
    print(" ", r)
mconn.close()
