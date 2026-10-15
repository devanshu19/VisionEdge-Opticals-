from werkzeug.security import generate_password_hash
import pymysql

# Configuration - matches .env DATABASE_URL: mysql+pymysql://root:@127.0.0.1:3306/visionedge_db
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'visionedge_db'

USERNAME = 'admin'
NEW_PASSWORD = 'admin@123'

def main():
    pw_hash = generate_password_hash(NEW_PASSWORD)
    print('Generated hash:', pw_hash)
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, port=DB_PORT)
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE `user` SET password_hash=%s WHERE username=%s", (pw_hash, USERNAME))
            conn.commit()
            print(f"Rows affected: {cur.rowcount}")
            if cur.rowcount == 0:
                print(f"Warning: no user named '{USERNAME}' found.")
            else:
                print(f"Password for user '{USERNAME}' updated successfully.")
    except Exception as e:
        print('Error updating password:', e)
    finally:
        conn.close()

if __name__ == '__main__':
    main()
