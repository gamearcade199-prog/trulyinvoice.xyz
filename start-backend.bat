@echo off
echo =======================================
echo TrulyInvoice - Backend Server
echo =======================================
echo.

cd /d "%~dp0backend"

echo [1/2] Activating Python virtual environment...
call venv\Scripts\activate.bat
echo.

echo [2/2] Starting FastAPI server...
echo.
echo =======================================
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Press CTRL+C to stop
echo =======================================
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
