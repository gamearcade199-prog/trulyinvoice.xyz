@echo off
echo ================================================
echo FIXING REACT WEBPACK ERROR
echo ================================================

echo Stopping development server (if running)...
taskkill /f /im node.exe >nul 2>&1

echo.
echo Navigating to frontend...
cd /d "C:\Users\akib\Desktop\trulyinvoice.in\frontend"

echo.
echo Removing .next build cache...
if exist .next rmdir /s /q .next

echo.
echo Removing package-lock.json...
if exist package-lock.json del package-lock.json

echo.
echo Clearing npm cache...
npm cache clean --force

echo.
echo Reinstalling packages...
npm install

echo.
echo Starting fresh development server...
npm run dev

pause