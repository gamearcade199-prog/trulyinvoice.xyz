@echo off
REM Start backend with API keys set - FOR WINDOWS
REM This ensures environment variables are loaded before Python starts

cd %~dp0backend

REM Set API Keys (replace with your actual keys)
set GOOGLE_AI_API_KEY=YOUR_GOOGLE_AI_API_KEY_HERE
set GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE

REM Activate venv and start backend
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload --port 8000 --log-level info

pause
