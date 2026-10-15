from werkzeug.security import generate_password_hash
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'visionedge.sqlite')
USERNAME = 'admin'
NEW_PASSWORD = 'admin@123'

if not os.path.exists(DB_PATH):
    print('SQLite DB not found at', DB_PATH)
    raise SystemExit(1)

pw_hash = generate_password_hash(NEW_PASSWORD)
print('Generated hash:', pw_hash)

conn = sqlite3.connect(DB_PATH)
try:
    cur = conn.cursor()
    cur.execute('UPDATE user SET password_hash=? WHERE username=?', (pw_hash, USERNAME))
    conn.commit()
    # sqlite3's rowcount may be -1 depending on version; use total_changes
    print('Total changes:', conn.total_changes)
    if conn.total_changes == 0:
        print(f"Warning: no user named '{USERNAME}' found or nothing changed.")
    else:
        print(f"Password for user '{USERNAME}' updated successfully in {DB_PATH}.")
finally:
    conn.close()
