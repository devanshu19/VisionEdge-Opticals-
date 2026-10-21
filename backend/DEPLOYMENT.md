# VisionEdge Production Deployment Guide
========================================

This guide details how to deploy the VisionEdge backend API (Flask + Supabase PostgreSQL architecture) into a production environment.

> **Important**: This backend is built on **Flask**, not Django. It exposes its existing application factory through `backend/wsgi.py` for WSGI servers.

---

## 1. Prerequisites
- Python 3.10+
- Supabase PostgreSQL Database (or any managed PostgreSQL 14+ instance)
- Environment Variables setup (`.env`)

---

## 2. Environment Variables Setup
Copy the `.env.example` file (or create `.env`) inside the `/backend` folder:
```env
DEBUG=False
SECRET_KEY="your-secure-flask-secret-key"
JWT_SECRET_KEY="your-secure-jwt-signature-key"
DATABASE_URL="postgresql+psycopg2://postgres.[project-ref]:[db-password]@aws-0-[region].pooler.supabase.com:6543/postgres"
DB_SSLMODE="require"
SUPABASE_URL="https://[project-ref].supabase.co"
SUPABASE_PUBLISHABLE_KEY="your-supabase-publishable-key"
FRONTEND_URL="https://your-frontend-domain.com"
```

---

## 3. Installation
Navigate to the `/backend` directory and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 4. Database Setup & Supabase Migration
The complete database schema for Supabase is located at:
`supabase/visionedge_complete_supabase_setup.sql`

### Option A: Via Supabase Dashboard (Recommended)
1. Open your project on [Supabase Dashboard](https://supabase.com/dashboard).
2. Go to **SQL Editor** -> **New query**.
3. Copy and paste the contents of `supabase/visionedge_complete_supabase_setup.sql` and click **Run**.
4. All 23 tables, foreign keys, triggers, and indexes are set up in one click.

### Option B: Automatic Schema Creation via SQLAlchemy
When running Flask in an environment with `DATABASE_URL` configured, SQLAlchemy will automatically ensure all tables are created on startup:
```bash
python manage.py db_check
```

---

## 5. Running the Application

### Development (Local testing)
```bash
python app.py
```

### Production (WSGI Options)

#### Option A: Gunicorn (Linux / Ubuntu / VPS / Render)
`gunicorn` is the industry standard for Python WSGI in Linux environments. A configuration file (`gunicorn_config.py`) is already provided.
```bash
gunicorn -c gunicorn_config.py "app:create_app()"
```

#### Option B: Waitress (Windows Environments)
If deploying onto Windows Server natively where Gunicorn is not supported, use `waitress`:
```bash
waitress-serve --port=5000 --call "app:create_app"
```

---

## 6. Deployment Guides

### Option 1: Render.com (Recommended PaaS)
1. Link your GitHub repository to Render as a **Web Service**.
2. Set **Root Directory** to `backend`.
3. Set **Build Command** to `pip install -r requirements.txt`.
4. Set **Start Command** to `gunicorn --bind 0.0.0.0:$PORT wsgi`.
5. Set `APP_ENV=production`, `DB_SSLMODE=require`, `PYTHON_VERSION=3.13.1`, and the required secrets listed in `render.yaml` in Render's Environment settings.
6. Set `FRONTEND_URL` to the deployed Netlify site origin (for example, `https://your-site.netlify.app`). Add any additional trusted HTTPS origins to `CORS_ALLOWED_ORIGINS` as a comma-separated list.
7. Configure the Razorpay webhook URL as `https://<your-render-service>.onrender.com/api/payment/razorpay/webhook` and use the same webhook secret in Render.

The existing `create_app()` factory is the only Flask application factory. The WSGI adapter does not create or register a second application. Production startup requires PostgreSQL and will fail rather than fall back to SQLite. Confirm the existing Supabase schema is already present before deploying; deployment does not create, migrate, or delete database data.

### Option 2: Ubuntu VPS (DigitalOcean, AWS EC2, Linode)
1. Install Python and Nginx:
   ```bash
   sudo apt update && sudo apt install python3-pip python3-venv nginx
   ```
2. Clone repository and configure `backend/.env` using your Supabase credentials.
3. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. Run Gunicorn as a systemd service (`/etc/systemd/system/visionedge.service`):
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
5. Setup Nginx Reverse Proxy (`/etc/nginx/sites-available/visionedge`):
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
6. Enable and restart Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/visionedge /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

---

## 7. Operational Monitoring

### Health Check Endpoint
To monitor uptime or link a load balancer, ping the health check route. It validates both the API runtime and the database connection:
- **GET** `/api/health`
- **Response**: `{"status": "running", "database": "connected", "dialect": "postgresql"}`
