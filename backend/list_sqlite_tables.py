import sqlite3, os
DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'visionedge.sqlite')
if not os.path.exists(DB_PATH):
    print('DB not found', DB_PATH)
    raise SystemExit(1)
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print('Tables:')
for r in cur.fetchall():
    print('-', r[0])
conn.close()
