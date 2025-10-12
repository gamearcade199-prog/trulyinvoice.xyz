# TrulyInvoice Frontend Fix Script
# Run this script to fix the Next.js SWC binary issue

Write-Host "=== TrulyInvoice Frontend Fix Script ===" -ForegroundColor Cyan
Write-Host ""

# Navigate to frontend directory
Set-Location C:\Users\akib\Desktop\trulyinvoice.in\frontend

Write-Host "[1/5] Stopping any running processes..." -ForegroundColor Yellow
# Kill any node processes on port 3000/3001
$processes = Get-Process -Name node -ErrorAction SilentlyContinue
if ($processes) {
    $processes | Stop-Process -Force
    Write-Host "  ✓ Stopped existing Node processes" -ForegroundColor Green
} else {
    Write-Host "  ✓ No running Node processes" -ForegroundColor Green
}

Write-Host ""
Write-Host "[2/5] Cleaning old files..." -ForegroundColor Yellow
# Remove node_modules
if (Test-Path "node_modules") {
    Write-Host "  - Removing node_modules (this may take a minute)..."
    Remove-Item -Recurse -Force node_modules
    Write-Host "  ✓ Removed node_modules" -ForegroundColor Green
} else {
    Write-Host "  ✓ node_modules already clean" -ForegroundColor Green
}

# Remove package-lock.json
if (Test-Path "package-lock.json") {
    Remove-Item -Force package-lock.json
    Write-Host "  ✓ Removed package-lock.json" -ForegroundColor Green
}

# Remove .next build cache
if (Test-Path ".next") {
    Remove-Item -Recurse -Force .next
    Write-Host "  ✓ Removed .next cache" -ForegroundColor Green
}

Write-Host ""
Write-Host "[3/5] Clearing npm cache..." -ForegroundColor Yellow
npm cache clean --force 2>&1 | Out-Null
Write-Host "  ✓ npm cache cleaned" -ForegroundColor Green

Write-Host ""
Write-Host "[4/5] Installing packages (this will take 2-3 minutes)..." -ForegroundColor Yellow
Write-Host "  Please wait..." -ForegroundColor Gray

# Install with verbose output
npm install --legacy-peer-deps

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Packages installed successfully!" -ForegroundColor Green
} else {
    Write-Host "  ✗ Installation failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    Write-Host ""
    Write-Host "ALTERNATIVE SOLUTIONS:" -ForegroundColor Yellow
    Write-Host "1. Downgrade Node.js to v20 LTS from: https://nodejs.org" -ForegroundColor Cyan
    Write-Host "2. Try upgrading Next.js: npm install next@latest" -ForegroundColor Cyan
    Write-Host "3. Check if any antivirus is blocking file operations" -ForegroundColor Cyan
    exit 1
}

Write-Host ""
Write-Host "[5/5] Starting development server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "=== STARTING NEXT.JS ===" -ForegroundColor Cyan
Write-Host "If you see the SWC error again, press CTRL+C and:" -ForegroundColor Yellow
Write-Host "  1. Download Node.js v20 LTS from https://nodejs.org" -ForegroundColor Cyan
Write-Host "  2. Install it" -ForegroundColor Cyan
Write-Host "  3. Run this script again" -ForegroundColor Cyan
Write-Host ""

# Start the dev server
npm run dev
