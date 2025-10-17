@echo off
REM Start backend with API keys set - FOR WINDOWS
REM This ensures environment variables are loaded before Python starts

cd %~dp0backend

REM Set API Keys
set GOOGLE_AI_API_KEY=AIzaSyBEnD60M9_JkSzUz_ZiBolN9pe5fDodPSE
set GEMINI_API_KEY=AIzaSyBEnD60M9_JkSzUz_ZiBolN9pe5fDodPSE

REM Activate venv and start backend
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload --port 8000 --log-level info

pause
