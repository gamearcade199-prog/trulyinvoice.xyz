@echo off
echo ========================================
echo   TrulyInvoice Backend Test Commands
echo   Complete Pipeline Testing Guide
echo ========================================
echo.

echo 1. START BACKEND SERVER:
echo    cd backend
echo    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.

echo 2. RUN PIPELINE TEST:
echo    cd backend
echo    python test_full_pipeline.py
echo.

echo 3. MANUAL TEST WITH CURL:
echo    curl http://localhost:8000/health
echo.

echo 4. CHECK LOGS:
echo    Look for Vision API calls and payment status normalization
echo.

echo ========================================
echo   Quick Commands to Copy/Paste
echo ========================================
echo.

echo START BACKEND:
echo cd c:\Users\akib\Desktop\trulyinvoice.in\backend
echo python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.

echo TEST PIPELINE (in new terminal):
echo cd c:\Users\akib\Desktop\trulyinvoice.in\backend
echo python test_full_pipeline.py
echo.

pause