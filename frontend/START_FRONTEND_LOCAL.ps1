# =====================================================
# Start Frontend Locally on Port 3000
# =====================================================
# This connects to the LOCAL backend on port 8000
# Make sure backend is running in another terminal!

$workspace = Split-Path -Parent $PSScriptRoot
$frontend = Join-Path $workspace "frontend"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 STARTING FRONTEND ON PORT 3000" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Location: $frontend" -ForegroundColor Gray
Write-Host "Frontend will connect to: http://localhost:8000" -ForegroundColor Gray
Write-Host ""
Write-Host "IMPORTANT:" -ForegroundColor Yellow
Write-Host "  1. Make sure backend is running in another terminal!" -ForegroundColor Yellow
Write-Host "  2. Open browser to: http://localhost:3000" -ForegroundColor Yellow
Write-Host "  3. Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Set-Location $frontend

# Install dependencies if needed
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies first..." -ForegroundColor Cyan
    npm install
}

# Start dev server
npm run dev
