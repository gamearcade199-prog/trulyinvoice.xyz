@echo off
echo ========================================
echo  Quick Push to GitHub
echo ========================================
echo.
echo Opening GitHub token page in your browser...
echo.
start https://github.com/settings/tokens/new?scopes=repo&description=TrulyInvoice
echo.
echo Follow these steps:
echo 1. The page will open in your browser
echo 2. Click "Generate token" at the bottom
echo 3. COPY the token (you'll only see it once!)
echo 4. Come back here and press any key
echo.
pause
echo.
echo Now let's push to GitHub...
echo.
echo When prompted:
echo - Username: gamearcade199-prog
echo - Password: PASTE THE TOKEN YOU JUST COPIED
echo.
pause
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo  SUCCESS! 
    echo ========================================
    echo.
    echo Your code is now on GitHub!
    echo Repository: https://github.com/gamearcade199-prog/trulyinvoice.xyz
    echo.
    echo Next: Go to https://vercel.com to deploy!
    echo.
) else (
    echo ========================================
    echo  FAILED!
    echo ========================================
    echo.
    echo Try again or use GitHub Desktop instead.
    echo Download: https://desktop.github.com/
    echo.
)
pause
