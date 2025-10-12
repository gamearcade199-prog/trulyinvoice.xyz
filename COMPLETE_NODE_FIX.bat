@echo off
echo ================================================
echo CHECKING NODE.JS VERSION AFTER INSTALLATION
echo ================================================

echo Refreshing environment variables...
call refreshenv

echo.
echo Current Node.js version:
node --version

echo.
echo Current npm version:
npm --version

echo.
echo Node.js installation location:
where node

echo.
echo ================================================
echo If you see v20.19.5 above, continue with Step 2
echo If you see v22.x.x, please:
echo 1. Close this terminal completely
echo 2. Open a new PowerShell window
echo 3. Run this script again
echo ================================================

echo.
echo STEP 2: Clean Frontend Installation
echo ================================================

echo Navigating to frontend directory...
cd /d "C:\Users\akib\Desktop\trulyinvoice.in\frontend"

echo.
echo Removing old installation files...
if exist node_modules (
    echo Removing node_modules...
    rmdir /s /q node_modules
) else (
    echo node_modules not found, skipping...
)

if exist package-lock.json (
    echo Removing package-lock.json...
    del package-lock.json
) else (
    echo package-lock.json not found, skipping...
)

if exist .next (
    echo Removing .next build cache...
    rmdir /s /q .next
) else (
    echo .next not found, skipping...
)

echo.
echo Clearing npm cache...
npm cache clean --force

echo.
echo Installing packages with Node.js v20...
npm install

echo.
echo ================================================
echo Installation complete! 
echo You can now run: npm run dev
echo ================================================
pause