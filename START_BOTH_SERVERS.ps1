Write-Host "🔧 FIXING TRULYINVOICE UPLOAD & RLS ISSUES" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Stop any running processes
Write-Host "🛑 Stopping existing processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like "*uvicorn*"} | Stop-Process -Force 2>$null
Get-Process node -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like "*next*"} | Stop-Process -Force 2>$null
Start-Sleep -Seconds 2

# Step 2: Start Backend
Write-Host "🚀 Starting backend server..." -ForegroundColor Green
cd "C:\Users\akib\Desktop\trulyinvoice.in\backend"
& .\venv\Scripts\Activate.ps1
$env:GOOGLE_AI_API_KEY="AIzaSyBEnD60M9_JkSzUz_ZiBolN9pe5fDodPSE"
$env:GEMINI_API_KEY="AIzaSyBEnD60M9_JkSzUz_ZiBolN9pe5fDodPSE"

# Start backend in background
Start-Process powershell -ArgumentList "-Command", "cd 'C:\Users\akib\Desktop\trulyinvoice.in\backend'; .\venv\Scripts\Activate.ps1; `$env:GOOGLE_AI_API_KEY='AIzaSyBEnD60M9_JkSzUz_ZiBolN9pe5fDodPSE'; python -m uvicorn app.main:app --reload --port 8000" -WindowStyle Minimized

Write-Host "⏳ Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Step 3: Test Backend
Write-Host "🔍 Testing backend connection..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/" -Method GET -TimeoutSec 10
    Write-Host "✅ Backend is running!" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend not responding. Check terminal for errors." -ForegroundColor Red
}

# Step 4: Start Frontend
Write-Host "🚀 Starting frontend server..." -ForegroundColor Green
cd "C:\Users\akib\Desktop\trulyinvoice.in\frontend"
Start-Process powershell -ArgumentList "-Command", "cd 'C:\Users\akib\Desktop\trulyinvoice.in\frontend'; npm run dev" -WindowStyle Minimized

Write-Host "⏳ Waiting for frontend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Step 5: Test Frontend
Write-Host "🔍 Testing frontend connection..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000/" -Method GET -TimeoutSec 10
    Write-Host "✅ Frontend is running!" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend not responding. Check terminal for errors." -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. Run the SQL fix in Supabase SQL Editor (see RLS_QUICK_FIX_GUIDE.md)" -ForegroundColor White
Write-Host "2. Test upload at: http://localhost:3000/upload" -ForegroundColor White
Write-Host "3. Check both terminals for any errors" -ForegroundColor White
Write-Host ""
Write-Host "🔗 Quick Links:" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Blue
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Blue
Write-Host "Upload:   http://localhost:3000/upload" -ForegroundColor Blue