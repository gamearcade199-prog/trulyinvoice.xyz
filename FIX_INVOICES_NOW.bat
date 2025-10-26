@echo off
echo ============================================================================
echo   FIX YOUR INVOICES - AUTOMATED SOLUTION
echo ============================================================================
echo.
echo This will:
echo   1. Stop any running backend
echo   2. Restart backend with fixes
echo   3. Process all your uploaded invoices
echo   4. Open browser to see results
echo.
pause

echo.
echo Step 1: Stopping any running backend...
taskkill /F /IM python.exe 2>nul
timeout /t 2 >nul

echo.
echo Step 2: Starting backend with fixes...
cd "%~dp0backend"
start "TrulyInvoice Backend" cmd /k "python -m uvicorn app.main:app --reload"

echo.
echo Waiting for backend to start...
timeout /t 5 >nul

echo.
echo Step 3: Processing your uploaded invoices...
cd "%~dp0"
python PROCESS_PENDING_DOCUMENTS.py

echo.
echo ============================================================================
echo   DONE! Now open your browser and:
echo   1. Go to http://localhost:3000/invoices
echo   2. Press Ctrl+Shift+R to refresh
echo   3. You should see all your invoices!
echo ============================================================================
echo.
pause
