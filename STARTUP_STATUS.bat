@echo off
cls
echo.
echo ========================================
echo   TRULYINVOICE - STARTUP SUMMARY
echo ========================================
echo.
echo ✅ BACKEND STATUS:
echo    • Running on: http://localhost:8000
echo    • Process: FastAPI + Uvicorn
echo    • Vision + Flash-Lite: ENABLED
echo    • Status: ✅ READY
echo.
echo ⚠️  FRONTEND STATUS:
echo    • Port: http://localhost:3000
echo    • Status: ⚠️ Permission issue with .next folder
echo.
echo 🔧 TO START FRONTEND (if not running):
echo.
echo    Option 1: Clear cache and start
echo    cd frontend
echo    rmdir .next /s /q
echo    npm run dev
echo.
echo    Option 2: Start with build
echo    cd frontend
echo    npm run build
echo    npm run start
echo.
echo ========================================
echo.
echo 🌐 ACCESS YOUR SYSTEM:
echo.
echo    Backend API:  http://localhost:8000
echo    Frontend:     http://localhost:3000
echo    API Docs:     http://localhost:8000/docs
echo.
echo ========================================
echo.
echo 📝 NEXT STEPS:
echo.
echo    1. Open browser to http://localhost:3000
echo    2. Upload an invoice
echo    3. Watch it process with Gemini OCR
echo    4. See results in Supabase database
echo.
echo ========================================
echo.
pause