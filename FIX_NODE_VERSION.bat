@echo off
echo ============================================
echo FIXING NODE.JS VERSION FOR TRULYINVOICE
echo ============================================

echo Checking current Node.js version...
node --version
npm --version

echo.
echo Cleaning frontend installation...
cd /d "C:\Users\akib\Desktop\trulyinvoice.in\frontend"

echo Removing node_modules and package-lock.json...
if exist node_modules rmdir /s /q node_modules
if exist package-lock.json del package-lock.json
if exist .next rmdir /s /q .next

echo.
echo Clearing npm cache...
npm cache clean --force

echo.
echo Reinstalling packages...
npm install

echo.
echo ============================================
echo If Node.js version shows v20.x.x above, 
echo you can now run: npm run dev
echo ============================================
pause