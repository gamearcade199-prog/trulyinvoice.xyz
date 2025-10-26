# Force clean frontend installation for Node.js v20
Write-Host "============================================" -ForegroundColor Green
Write-Host "FORCE CLEANING FRONTEND FOR NODE.JS v20" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green

# Check Node.js version
Write-Host "Current Node.js version:" -ForegroundColor Yellow
node --version

# Navigate to frontend directory
Set-Location "C:\Users\akib\Desktop\trulyinvoice.in\frontend"
Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow

# Force stop any Node.js processes
Write-Host "`nStopping any running Node.js processes..." -ForegroundColor Yellow
Get-Process -Name "node" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Wait a moment
Start-Sleep -Seconds 2

# Force remove node_modules with different methods
Write-Host "`nRemoving node_modules directory..." -ForegroundColor Yellow
if (Test-Path "node_modules") {
    try {
        # Method 1: Standard removal
        Remove-Item -Recurse -Force "node_modules" -ErrorAction Stop
        Write-Host "✓ node_modules removed successfully" -ForegroundColor Green
    }
    catch {
        Write-Host "Standard removal failed, trying alternative methods..." -ForegroundColor Red
        
        # Method 2: Use robocopy to clear (Windows trick)
        $emptyDir = "$env:TEMP\empty_dir_$(Get-Random)"
        New-Item -ItemType Directory -Path $emptyDir -Force | Out-Null
        robocopy $emptyDir "node_modules" /MIR /NP /NJH /NJS
        Remove-Item -Recurse -Force $emptyDir -ErrorAction SilentlyContinue
        Remove-Item -Recurse -Force "node_modules" -ErrorAction SilentlyContinue
        
        if (Test-Path "node_modules") {
            Write-Host "⚠ Some files may still be locked. Please manually delete node_modules folder." -ForegroundColor Red
        } else {
            Write-Host "✓ node_modules removed with alternative method" -ForegroundColor Green
        }
    }
} else {
    Write-Host "✓ node_modules already removed" -ForegroundColor Green
}

# Remove other files
Write-Host "`nRemoving package-lock.json..." -ForegroundColor Yellow
Remove-Item -Force "package-lock.json" -ErrorAction SilentlyContinue

Write-Host "Removing .next directory..." -ForegroundColor Yellow
Remove-Item -Recurse -Force ".next" -ErrorAction SilentlyContinue

# Clear npm cache
Write-Host "`nClearing npm cache..." -ForegroundColor Yellow
npm cache clean --force

# Fresh install
Write-Host "`nInstalling packages with Node.js v20..." -ForegroundColor Yellow
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ SUCCESS! Frontend packages installed successfully!" -ForegroundColor Green
    Write-Host "`nTrying to start development server..." -ForegroundColor Yellow
    npm run dev
} else {
    Write-Host "`n❌ Installation failed. Manual intervention needed." -ForegroundColor Red
    Write-Host "`nTry manually deleting the node_modules folder and running:" -ForegroundColor Yellow
    Write-Host "npm install" -ForegroundColor Cyan
}

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")