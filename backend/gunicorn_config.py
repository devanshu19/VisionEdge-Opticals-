import multiprocessing
import os

# Gunicorn configuration file
# Can be run via: gunicorn -c gunicorn_config.py "app:create_app()"

# Bind to 0.0.0.0 on port 8000 (standard production port, adjust if needed)
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8000')

# Worker configuration (Recommended: (2 x $num_cores) + 1)
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'  # Use 'gevent' or 'eventlet' for async processing if needed
worker_connections = 1000

# Timeouts
timeout = 120
keepalive = 2

# Logging
errorlog = 'logs/gunicorn-error.log'
accesslog = 'logs/gunicorn-access.log'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process Naming
proc_name = 'visionedge_wsgi'

def on_starting(server):
    print(f"Starting VisionEdge WSGI Server with {workers} workers.")
