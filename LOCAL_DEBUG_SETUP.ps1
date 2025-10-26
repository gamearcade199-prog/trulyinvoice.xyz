# TRULYINVOICE LOCAL DEBUG SETUP
# Install dependencies and setup local environment

$workspace = $PSScriptRoot
$backend = Join-Path $workspace "backend"
$frontend = Join-Path $workspace "frontend"

Write-Host "Setting up backend..."
Set-Location $backend

if (-not (Test-Path "venv")) {
    python -m venv venv
}

& ".\venv\Scripts\Activate.ps1"
pip install -r requirements.txt -q

Write-Host "Setting up frontend..."
Set-Location $frontend

if (-not (Test-Path "node_modules")) {
    npm install -q
}

Write-Host ""
Write-Host "SETUP COMPLETE!"
Write-Host ""
Write-Host "To start debugging, run these in separate terminals:"
Write-Host ""
Write-Host "Terminal 1 - Backend:"
Write-Host "  cd $backend"
Write-Host "  .\\venv\\Scripts\\Activate.ps1"
Write-Host "  python -m uvicorn app.main:app --reload --port 8000 --log-level debug"
Write-Host ""
Write-Host "Terminal 2 - Frontend:"
Write-Host "  cd $frontend"
Write-Host "  npm run dev"
Write-Host ""
Write-Host "Then open http://localhost:3000 in your browser"
