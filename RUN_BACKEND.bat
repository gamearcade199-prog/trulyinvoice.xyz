@echo off
echo ========================================
echo   Starting TrulyInvoice Backend
echo ========================================
echo.

cd /d "C:\Users\akib\Desktop\trulyinvoice.in\backend"

echo Backend directory: %CD%
echo.
echo Starting FastAPI server on port 8000...
echo Press CTRL+C to stop the server
echo.
echo ========================================

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

echo.
echo Server stopped.
pause
