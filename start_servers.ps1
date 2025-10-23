Write-Host "Starting TrulyInvoice Servers..." -ForegroundColor Green

# Stop existing processes
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like "*uvicorn*"} | Stop-Process -Force 2>$null
Get-Process node -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like "*next*"} | Stop-Process -Force 2>$null
Start-Sleep -Seconds 2

Write-Host "Starting Backend..." -ForegroundColor Yellow
cd "C:\Users\akib\Desktop\trulyinvoice.in\backend"
$env:GOOGLE_AI_API_KEY="YOUR_NEW_GOOGLE_AI_API_KEY_HERE"
Start-Process powershell -ArgumentList "-Command", "cd 'C:\Users\akib\Desktop\trulyinvoice.in\backend'; .\venv\Scripts\Activate.ps1; `$env:GOOGLE_AI_API_KEY='YOUR_NEW_GOOGLE_AI_API_KEY_HERE'; python -m uvicorn app.main:app --reload --port 8000" -WindowStyle Normal

Start-Sleep -Seconds 3

Write-Host "Starting Frontend..." -ForegroundColor Yellow
cd "C:\Users\akib\Desktop\trulyinvoice.in\frontend"
Start-Process powershell -ArgumentList "-Command", "cd 'C:\Users\akib\Desktop\trulyinvoice.in\frontend'; npm run dev" -WindowStyle Normal

Write-Host "Servers starting... Check the new terminal windows." -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Blue
Write-Host "Backend: http://localhost:8000" -ForegroundColor Blue