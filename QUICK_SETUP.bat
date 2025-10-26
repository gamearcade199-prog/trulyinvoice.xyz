@echo off
echo ========================================
echo TrulyInvoice - Quick Setup
echo ========================================
echo.

echo [1/5] Installing Backend Dependencies...
cd backend
pip install -r requirements.txt
echo.

echo [2/5] Installing Frontend Dependencies...
cd ..\frontend
call npm install
echo.

echo [3/5] Creating Environment Files...
cd ..\backend
if not exist .env (
    copy .env.example .env
    echo Created backend\.env - Please add your API keys!
) else (
    echo backend\.env already exists
)
echo.

cd ..\frontend
if not exist .env.local (
    echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
    echo Created frontend\.env.local
) else (
    echo frontend\.env.local already exists
)
echo.

echo [4/5] Initializing Database...
cd ..\backend
python -c "from app.database import init_db; init_db()"
echo Database tables created!
echo.

echo [5/5] Setup Complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo 1. Add your API keys to backend\.env
echo    - RAZORPAY_KEY_ID (get from https://dashboard.razorpay.com)
echo    - RAZORPAY_KEY_SECRET
echo    - DATABASE_URL
echo.
echo 2. Start the backend:
echo    cd backend
echo    python -m uvicorn app.main:app --reload --port 8000
echo.
echo 3. Start the frontend (in new terminal):
echo    cd frontend
echo    npm run dev
echo.
echo 4. Open http://localhost:3000
echo ========================================
pause
