@echo off
echo =======================================
echo TrulyInvoice - Frontend Setup
echo =======================================
echo.

cd /d "%~dp0frontend"

echo [1/5] Cleaning old files...
if exist node_modules (
    echo Removing node_modules...
    rmdir /s /q node_modules
)
if exist package-lock.json (
    del /f /q package-lock.json
)
if exist .next (
    rmdir /s /q .next
)
if exist .babelrc (
    echo Removing .babelrc...
    del /f /q .babelrc
)
echo Done!
echo.

echo [2/5] Installing packages...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: npm install failed!
    echo.
    echo Try installing Node.js v20 from: https://nodejs.org
    pause
    exit /b 1
)
echo.

echo [3/5] Installing @babel/runtime (required)...
call npm install @babel/runtime
echo.

echo [4/5] Cleaning build cache...
if exist .next (
    rmdir /s /q .next
)
echo.

echo [5/5] Starting development server...
echo.
echo =======================================
echo Frontend will be at: http://localhost:3000
echo Press CTRL+C to stop
echo =======================================
echo.

call npm run dev
