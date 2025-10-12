@echo off
echo ============================================
echo FORCE CLEAN FRONTEND - NODE.JS v20 FIX
echo ============================================

echo Checking Node.js version...
node --version

echo.
echo Navigating to frontend directory...
cd /d "C:\Users\akib\Desktop\trulyinvoice.in\frontend"

echo.
echo Stopping any running Node.js processes...
taskkill /f /im node.exe >nul 2>&1

echo.
echo Force removing node_modules...
if exist node_modules (
    echo Attempting standard removal...
    rmdir /s /q node_modules >nul 2>&1
    
    if exist node_modules (
        echo Standard removal failed, using robocopy method...
        mkdir "%TEMP%\empty_dir_%RANDOM%" >nul 2>&1
        robocopy "%TEMP%\empty_dir_%RANDOM%" node_modules /MIR /NP /NJH /NJS >nul 2>&1
        rmdir /s /q node_modules >nul 2>&1
        rmdir /s /q "%TEMP%\empty_dir_%RANDOM%" >nul 2>&1
    )
    
    if exist node_modules (
        echo WARNING: Some files may still be locked.
        echo Please manually delete the node_modules folder in File Explorer
        echo Then run this script again.
        pause
        exit /b 1
    ) else (
        echo SUCCESS: node_modules removed
    )
) else (
    echo node_modules already removed
)

echo.
echo Removing other files...
if exist package-lock.json del /f package-lock.json >nul 2>&1
if exist .next rmdir /s /q .next >nul 2>&1

echo.
echo Clearing npm cache...
npm cache clean --force

echo.
echo Installing packages with Node.js v20...
npm install

if %errorlevel% equ 0 (
    echo.
    echo ============================================
    echo SUCCESS! Installation completed!
    echo ============================================
    echo.
    echo Starting development server...
    npm run dev
) else (
    echo.
    echo ============================================
    echo INSTALLATION FAILED
    echo ============================================
    echo Please manually delete node_modules folder
    echo and try running: npm install
    echo.
)

pause