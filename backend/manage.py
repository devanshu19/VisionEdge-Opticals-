import os
import sys
import argparse
from datetime import datetime
import subprocess
from dotenv import load_dotenv

def backup_database():
    load_dotenv()
    db_url = os.environ.get('DATABASE_URL')
    
    if not db_url or "mysql" not in db_url:
        print("Error: MySQL DATABASE_URL not found in .env")
        sys.exit(1)
        
    # Extract DB details roughly (mysql+pymysql://user:pass@host:port/dbname)
    # Simple parse for demo/production script
    try:
        parts = db_url.split('://')[1].split('/')
        db_name = parts[1].split('?')[0]
        credentials, host_port = parts[0].split('@')
        user = credentials.split(':')[0]
        password = credentials.split(':')[1] if ':' in credentials else ''
        host = host_port.split(':')[0]
    except Exception as e:
        print(f"Failed to parse database URL: {e}")
        sys.exit(1)
        
    backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f'backup_{date_str}.sql')
    
    print(f"Starting backup for database '{db_name}'...")
    
    cmd = ['mysqldump', '-u', user, '-h', host, db_name]
    if password:
        cmd.insert(2, f'-p{password}')
        
    try:
        with open(backup_file, 'w') as f:
            subprocess.run(cmd, stdout=f, check=True)
        print(f"Backup successful! Saved to: {backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e}")
        if os.path.exists(backup_file):
            os.remove(backup_file)
    except FileNotFoundError:
        print("Error: 'mysqldump' not found in PATH. Please install MySQL client tools.")

def main():
    parser = argparse.ArgumentParser(description="VisionEdge Management CLI")
    parser.add_argument('command', help="Command to run (e.g., backup_database)")
    
    args = parser.parse_args()
    
    if args.command == 'backup_database':
        backup_database()
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()

if __name__ == '__main__':
    main()
