@echo off
echo =======================================
echo Quick Fix for Babel Runtime Error
echo =======================================
echo.

cd /d "%~dp0frontend"

echo [1/3] Stopping any running servers...
echo Press CTRL+C in the frontend window to stop it first!
echo.
pause
echo.

echo [2/3] Installing @babel/runtime...
call npm install @babel/runtime
echo.

echo [3/3] Removing .babelrc and .next cache...
if exist .babelrc (
    del /f /q .babelrc
    echo Removed .babelrc
)
if exist .next (
    rmdir /s /q .next
    echo Removed .next cache
)
echo.

echo =======================================
echo Fix applied! Now run:
echo   start-frontend.bat
echo =======================================
pause
