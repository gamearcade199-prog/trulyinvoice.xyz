# =====================================================
# Start Backend Locally with Full Logging
# =====================================================
# Run this in a dedicated terminal window
# It will show all backend logs in real-time

$workspace = Split-Path -Parent $PSScriptRoot
$backend = Join-Path $workspace "backend"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 STARTING BACKEND ON PORT 8000" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Location: $backend" -ForegroundColor Gray
Write-Host "Command: uvicorn app.main:app --reload --port 8000 --log-level debug" -ForegroundColor Gray
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Set-Location $backend

# Activate venv if it exists
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    & ".\venv\Scripts\Activate.ps1"
}

# Start uvicorn with debug logging
python -m uvicorn app.main:app --reload --port 8000 --log-level debug
