# TrulyInvoice Backend Start Script

Write-Host "=== TrulyInvoice Backend Server ===" -ForegroundColor Cyan
Write-Host ""

# Navigate to backend directory
Set-Location C:\Users\akib\Desktop\trulyinvoice.in\backend

Write-Host "[1/3] Activating Python virtual environment..." -ForegroundColor Yellow
# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"
Write-Host "  ✓ Virtual environment activated" -ForegroundColor Green

Write-Host ""
Write-Host "[2/3] Checking environment variables..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  ✓ .env file found" -ForegroundColor Green
} else {
    Write-Host "  ✗ .env file missing!" -ForegroundColor Red
    Write-Host "  Please create .env file with required API keys" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "[3/3] Starting FastAPI server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "=== SERVER STARTING ===" -ForegroundColor Cyan
Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor Green
Write-Host "API Documentation (Swagger): http://localhost:8000/docs" -ForegroundColor Green
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
