@echo off
REM Deploy fixes to Render
echo.
echo ========================================
echo  DEPLOYING FIXES TO RENDER
echo ========================================
echo.

REM Check if git is available
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed or not in PATH
    exit /b 1
)

REM Add all changes
echo [1/3] Adding changes...
git add .
if %errorlevel% neq 0 (
    echo ERROR: Failed to add changes
    exit /b 1
)
echo ✅ Changes added

REM Commit
echo [2/3] Committing changes...
git commit -m "Fix: Subscription query PGRST116, add Vision API, fix user signup - Render production hotfix"
if %errorlevel% neq 0 (
    echo ERROR: Failed to commit changes
    exit /b 1
)
echo ✅ Changes committed

REM Push
echo [3/3] Pushing to GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo ERROR: Failed to push to GitHub
    exit /b 1
)
echo ✅ Pushed to GitHub

echo.
echo ========================================
echo  NEXT STEPS
echo ========================================
echo.
echo 1. Go to: https://dashboard.render.com
echo 2. Click "trulyinvoice-backend" service
echo 3. Click "Manual Deploy" → "Deploy latest commit"
echo 4. Wait 1-2 minutes for deployment
echo 5. Check logs for "Application startup complete"
echo.
echo ========================================
echo  VERIFY DEPLOYMENT
echo ========================================
echo.
echo Test endpoints:
echo - Health: GET https://trulyinvoice-backend.onrender.com/
echo - Docs: GET https://trulyinvoice-backend.onrender.com/docs
echo.
echo Expected results:
echo ✅ New user signup creates subscription
echo ✅ Invoice processing works
echo ✅ No PGRST116 errors
echo.
pause
