import sqlite3

def migrate():
    conn = sqlite3.connect('backend/instance/visionedge.db')
    c = conn.cursor()
    
    columns_to_add = [
        ("prescription_number", "VARCHAR(50)"),
        ("doctor_name", "VARCHAR(100)"),
        ("status", "VARCHAR(20) DEFAULT 'Completed'"),
        ("od_prism", "VARCHAR(10)"),
        ("od_base", "VARCHAR(10)"),
        ("od_va", "VARCHAR(10)"),
        ("os_prism", "VARCHAR(10)"),
        ("os_base", "VARCHAR(10)"),
        ("os_va", "VARCHAR(10)"),
        ("distance_pd", "VARCHAR(10)"),
        ("near_pd", "VARCHAR(10)"),
        ("lens_type", "VARCHAR(50)"),
        ("lens_material", "VARCHAR(50)"),
        ("lens_coating", "VARCHAR(100)"),
        ("frame_recommendation", "VARCHAR(200)"),
        ("lens_recommendation", "VARCHAR(200)"),
        ("source", "VARCHAR(50) DEFAULT 'Manual Entry'"),
        ("created_by", "INTEGER"),
        ("created_at", "DATETIME"),
        ("updated_at", "DATETIME")
    ]
    
    for col_name, col_type in columns_to_add:
        try:
            c.execute(f"ALTER TABLE prescription ADD COLUMN {col_name} {col_type}")
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
