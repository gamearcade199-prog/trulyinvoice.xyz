@echo off
echo ========================================
echo   TrulyInvoice Backend Server
echo   Starting FastAPI on http://localhost:8000
echo ========================================
echo.

cd /d "%~dp0"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
