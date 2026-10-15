import sqlite3

def migrate():
    conn = sqlite3.connect('backend/instance/visionedge.db')
    c = conn.cursor()
    
    try:
        c.execute("ALTER TABLE customer ADD COLUMN customer_code VARCHAR(20)")
        print("Added column customer_code")
    except sqlite3.OperationalError as e:
        print(f"Error adding customer_code: {e}")
                
    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate()
