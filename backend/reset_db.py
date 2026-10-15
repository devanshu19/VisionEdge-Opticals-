import pymysql

# Connect to MySQL server (without specifying database)
try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        port=3306
    )
    
    with connection.cursor() as cursor:
        cursor.execute("DROP DATABASE IF EXISTS visionedge_db;")
        cursor.execute("CREATE DATABASE visionedge_db;")
        print("Successfully dropped and recreated 'visionedge_db' database.")
        
    connection.commit()
    connection.close()
except Exception as e:
    print(f"Error connecting to MySQL: {e}")
