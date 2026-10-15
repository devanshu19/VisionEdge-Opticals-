import os
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "visionedge_db")

def get_db_connection():
    """Establishes a direct connection to XAMPP MySQL server."""
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=DictCursor,
        autocommit=True
    )
    return connection

def execute_query(sql, params=None):
    """Executes an INSERT/UPDATE/DELETE query on XAMPP MySQL."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.lastrowid
    finally:
        conn.close()

def fetch_all(sql, params=None):
    """Executes a SELECT query and returns all matching rows as dictionaries."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.fetchall()
    finally:
        conn.close()

def fetch_one(sql, params=None):
    """Executes a SELECT query and returns a single row as a dictionary."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.fetchone()
    finally:
        conn.close()

if __name__ == '__main__':
    try:
        conn = get_db_connection()
        print(f"Successfully connected directly to XAMPP MySQL database '{DB_NAME}' on {DB_HOST}:{DB_PORT}!")
        conn.close()
    except Exception as e:
        print(f"Error connecting to XAMPP MySQL: {e}")
