# Start the backend Flask server in a new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; if (!(Test-Path venv)) { python -m venv venv }; .\venv\Scripts\activate; pip install -r requirements.txt; python app.py"

# Start the frontend static server in the current window
Write-Host "Starting Frontend Server..."
cd frontend
python server.py
