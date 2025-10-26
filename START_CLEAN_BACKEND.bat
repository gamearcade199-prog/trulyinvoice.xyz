@echo off
cls
echo.
echo ============================================================
echo   TRULYINVOICE BACKEND V2.0 - CLEAN ARCHITECTURE
echo   No dependency conflicts, Python 3.14 compatible
echo ============================================================
echo.

REM Kill any existing Python processes
echo [1/3] Stopping any running backend instances...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 /nobreak >nul

REM Navigate to backend directory
cd /d "%~dp0backend"

REM Set Python path
set PYTHONPATH=%~dp0backend

echo [2/3] Starting FastAPI backend server...
echo.
echo Backend will run on: http://localhost:8000
echo API Docs available at: http://localhost:8000/docs
echo.
echo [3/3] Server starting... (Press CTRL+C to stop)
echo.

REM Start the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
