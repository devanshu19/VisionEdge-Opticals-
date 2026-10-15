# VisionEdge Production Deployment Guide

This guide details how to deploy the VisionEdge backend API (Flask + MySQL architecture) into a production environment. 

> **Important**: This backend is built on **Flask**, not Django. Standard Django commands (`manage.py runserver`, `collectstatic`, `wsgi.py`) have been replaced by robust Flask WSGI alternatives.

---

## 1. Prerequisites
- Python 3.9+
- MySQL Server 8.0+
- Environment Variables setup (`.env`)

## 2. Environment Variables Setup
Copy the `.env.example` file (or create `.env`) inside the `/backend` folder:
```env
DEBUG=False
SECRET_KEY="your-secure-flask-secret-key"
JWT_SECRET_KEY="your-secure-jwt-signature-key"
DATABASE_URL="mysql+pymysql://username:password@localhost:3306/visionedge_db"
GEMINI_API_KEY="your-optional-google-gemini-key"
```

## 3. Installation
Navigate to the `/backend` directory and install the exact locked dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Database Setup & Migrations
Because we are using standard SQLAlchemy (without Django ORM), migrations are handled via custom initialization scripts:
```bash
# 1. First, create the database and tables natively:
python setup_mysql.py

# 2. Run the data migration/seeding script (if applying initial schema structure):
python migrate_mysql.py
```
*Note: Your `DATABASE_URL` in `.env` must accurately reflect the MySQL credentials.*

## 5. Running the Application

### Development (Local testing only)
```bash
python app.py
```

### Production (WSGI Options)

#### Option A: Gunicorn (Linux/Ubuntu/VPS/Render)
`gunicorn` is the industry standard for Python WSGI in Linux environments. A configuration file (`gunicorn_config.py`) is already provided.
```bash
gunicorn -c gunicorn_config.py "app:create_app()"
```

#### Option B: Waitress (Windows Environments)
If deploying onto a Windows Server natively where Gunicorn isn't supported, use `waitress`:
```bash
waitress-serve --port=8000 --call "app:create_app"
```

---

## 6. Deployment Guides

### Option 1: Render.com (Recommended PaaS)
1. Link your GitHub repository to Render as a **Web Service**.
2. **Environment**: Python
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `gunicorn -c gunicorn_config.py "app:create_app()"`
5. **Environment Variables**: Add `DATABASE_URL` (link to a managed MySQL DB), `SECRET_KEY`, `JWT_SECRET_KEY`, and `DEBUG=False` in Render's Secret Manager.

### Option 2: Ubuntu VPS (DigitalOcean, AWS EC2, Linode)
1. Install Python and Nginx: `sudo apt update && sudo apt install python3-pip python3-venv nginx mysql-server`.
2. Clone the repository and configure `.env` using your MySQL credentials.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run Gunicorn as a systemd service. Create `/etc/systemd/system/visionedge.service`:
   ```ini
   [Unit]
   Description=Gunicorn instance to serve VisionEdge
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/VisionEdge/backend
   Environment="PATH=/path/to/VisionEdge/backend/venv/bin"
   ExecStart=/path/to/VisionEdge/backend/venv/bin/gunicorn -c gunicorn_config.py "app:create_app()"

   [Install]
   WantedBy=multi-user.target
   ```
5. Setup Nginx Reverse Proxy inside `/etc/nginx/sites-available/visionedge`:
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
6. Restart Nginx: `sudo systemctl restart nginx`.

### Option 3: PythonAnywhere
1. Create a Web App configured with Python 3.9+.
2. Under the WSGI Configuration file provided by PythonAnywhere, configure the import to launch the Flask app:
   ```python
   import sys
   import os
   from dotenv import load_dotenv

   path = '/home/yourusername/VisionEdge/backend'
   if path not in sys.path:
       sys.path.append(path)

   # Load .env
   load_dotenv(os.path.join(path, '.env'))

   from app import create_app
   application = create_app()
   ```
3. `whitenoise` will automatically handle static assets gracefully.

---

## 7. Operational Monitoring

### Health Check Endpoint
To monitor uptime or link a load balancer, ping the health check route. It validates both the API runtime and the MySQL connection.
- **GET** `/api/health`
- **Response**: `{"status": "running", "database": "connected"}`

### Backups
To take a manual snapshot of the MySQL database safely without stopping Gunicorn:
```bash
python manage.py backup_database
```
*Creates a `.sql` artifact inside the `/backups/` directory.*
