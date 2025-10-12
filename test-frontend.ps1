# Check Node.js version and test frontend
Write-Host "Node.js version:"
node --version

Write-Host "NPM version:"
npm --version

Write-Host "Current directory:"
Get-Location

Write-Host "Changing to frontend directory..."
Set-Location "C:\Users\akib\Desktop\trulyinvoice.in\frontend"

Write-Host "Frontend directory contents:"
Get-ChildItem | Select-Object Name, Length

Write-Host "Attempting to start frontend..."
npm run dev