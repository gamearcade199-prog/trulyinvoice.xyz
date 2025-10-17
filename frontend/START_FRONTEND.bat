@echo off
REM =====================================================
REM START FRONTEND LOCALLY
REM Make sure backend is running in another terminal!
REM =====================================================

cd /d "%~dp0frontend"

REM Check if node_modules exists
if not exist node_modules (
    echo Installing npm dependencies...
    call npm install
)

REM Start dev server
echo.
echo ========================================
echo Starting frontend on http://localhost:3000
echo ========================================
echo.
call npm run dev

pause
