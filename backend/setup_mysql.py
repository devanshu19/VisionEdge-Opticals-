import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "visionedge_db")

print(f"Connecting to XAMPP MySQL Server at {DB_HOST}:{DB_PORT} as user '{DB_USER}'...")

try:
    # 1. Connect without database to ensure database exists
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD
    )
    with conn.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print("[OK] Verified/Created MySQL Database '" + DB_NAME + "' in XAMPP.")
    conn.commit()
    conn.close()

    # 2. Connect to visionedge_db and run visionedge_xampp_mysql.sql dump
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    
    sql_file_path = os.path.join(os.path.dirname(__file__), 'visionedge_xampp_mysql.sql')
    if os.path.exists(sql_file_path):
        print("Reading SQL DDL script from " + sql_file_path + "...")
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # Split SQL statements by semicolon
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]
        
        with conn.cursor() as cursor:
            for statement in statements:
                if statement.startswith('--') or statement.startswith('/*'):
                    continue
                try:
                    cursor.execute(statement)
                except Exception as stmt_err:
                    print("Warning on statement: " + str(stmt_err))

        conn.commit()
        print("[OK] Successfully executed SQL schema import into XAMPP MySQL!")
    else:
        print("Error: SQL file " + sql_file_path + " not found.")

    conn.close()
    print("=======================================================")
    print("VisionEdge is now fully connected to XAMPP MySQL Database '" + DB_NAME + "'!")
    print("=======================================================")

except Exception as e:
    print("\n[ERROR] Could not connect to XAMPP MySQL server.")
    print("Error Details: " + str(e))
    print("\nPlease verify:")
    print(" 1. XAMPP Control Panel is open and MySQL service is started.")
    print(" 2. MySQL is running on port " + str(DB_PORT) + ".")
    print(" 3. User '" + str(DB_USER) + "' has permissions and password is correct.")
