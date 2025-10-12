@echo off
echo ========================================
echo  TrulyInvoice - Push to GitHub
echo ========================================
echo.

echo Checking git status...
git status
echo.

echo ========================================
echo  AUTHENTICATION REQUIRED
echo ========================================
echo.
echo You will need:
echo 1. GitHub Username: gamearcade199-prog
echo 2. Personal Access Token (NOT your password!)
echo.
echo Get your token at:
echo https://github.com/settings/tokens
echo.
echo Press any key to push to GitHub...
pause >nul

echo.
echo Pushing to GitHub...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  SUCCESS! Code pushed to GitHub!
    echo ========================================
    echo.
    echo Repository: https://github.com/gamearcade199-prog/trulyinvoice.xyz
    echo.
    echo Next steps:
    echo 1. Go to https://vercel.com
    echo 2. Import your repository
    echo 3. Deploy your app!
    echo.
) else (
    echo.
    echo ========================================
    echo  PUSH FAILED!
    echo ========================================
    echo.
    echo Common reasons:
    echo 1. Wrong username or token
    echo 2. Token doesn't have 'repo' scope
    echo 3. Not authenticated
    echo.
    echo See PUSH_TO_GITHUB.md for help
    echo.
)

pause
