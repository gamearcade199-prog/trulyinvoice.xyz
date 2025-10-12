@echo off
echo ============================================
echo TESTING FRONTEND WITH NODE.JS v20
echo ============================================

echo Current Node.js version:
node --version

echo.
echo Navigating to frontend directory...
cd /d "C:\Users\akib\Desktop\trulyinvoice.in\frontend"

echo.
echo Current directory:
cd

echo.
echo Starting frontend development server...
echo This should work without SWC binary errors now!
echo.
npm run dev

pause