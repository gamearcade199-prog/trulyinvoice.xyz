Write-Host "Fixing line endings..." -ForegroundColor Cyan

$files = @(
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\upload\page.tsx",
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\invoices\page.tsx",
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\invoices\[id]\page.tsx",
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\dashboard\settings\page.tsx",
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\dashboard\support\page.tsx",
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\dashboard\pricing\page.tsx",
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\page.tsx",
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\about\page.tsx",
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\contact\page.tsx",
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\features\page.tsx",
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\careers\page.tsx",
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\security\page.tsx",
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\privacy\page.tsx",
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\terms\page.tsx",
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\forgot-password\page.tsx",
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\pricing\page.tsx"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        $content = Get-Content -Path $file -Raw
        Set-Content -Path $file -Value $content
        Write-Host "Fixed: $file" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Line endings fixed!" -ForegroundColor Cyan
