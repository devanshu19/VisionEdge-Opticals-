import sqlite3

def migrate():
    conn = sqlite3.connect('backend/instance/visionedge.db')
    c = conn.cursor()
    
    columns_to_add = [
        ("customer_code", "VARCHAR(20) UNIQUE"),
        ("alternate_phone", "VARCHAR(20)"),
        ("occupation", "VARCHAR(100)"),
        ("city", "VARCHAR(100)"),
        ("state", "VARCHAR(100)"),
        ("pincode", "VARCHAR(20)"),
        ("emergency_contact", "VARCHAR(100)"),
        ("emergency_phone", "VARCHAR(20)"),
        ("blood_group", "VARCHAR(10)"),
        ("photo", "VARCHAR(255)"),
        ("eye_condition", "TEXT"),
        ("lens_preference", "VARCHAR(100)"),
        ("frame_preference", "VARCHAR(100)"),
        ("doctor_name", "VARCHAR(100)"),
        ("status", "VARCHAR(20) DEFAULT 'Active'"),
        ("updated_at", "DATETIME"),
        ("created_by", "INTEGER")
    ]
    
    for col_name, col_type in columns_to_add:
        try:
            c.execute(f"ALTER TABLE customer ADD COLUMN {col_name} {col_type}")
            print(f"Added column {col_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print(f"Column {col_name} already exists.")
            else:
                print(f"Error adding {col_name}: {e}")
                
    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate()
