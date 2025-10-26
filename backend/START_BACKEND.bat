@echo off
REM =====================================================
REM START BACKEND LOCALLY WITH DEBUGGING
REM =====================================================

cd /d "%~dp0backend"

REM Check if venv exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install fastapi uvicorn python-dotenv pydantic pydantic-settings email-validator python-multipart requests PyPDF2 reportlab openpyxl Pillow supabase openai google-generativeai razorpay sqlalchemy passlib pyotp slowapi -q

REM Start server
echo.
echo ========================================
echo Starting backend on http://localhost:8000
echo ========================================
echo.
python -m uvicorn app.main:app --reload --port 8000 --log-level debug

pause
