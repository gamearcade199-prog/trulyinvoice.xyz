Write-Host "Starting theme update..." -ForegroundColor Cyan

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
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\login\page.tsx",
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\register\page.tsx",
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\forgot-password\page.tsx",
    "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\pricing\page.tsx"
)

$count = 0

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "Updating: $file" -ForegroundColor Yellow
        
        $content = Get-Content -Path $file -Raw
        $original = $content
        
        $content = $content -replace 'bg-white dark:bg-gray-800', 'bg-gray-50 dark:bg-gray-900'
        $content = $content -replace 'border-gray-200 dark:border-gray-700', 'border-gray-200 dark:border-gray-800'
        $content = $content -replace 'divide-gray-200 dark:divide-gray-700', 'divide-gray-200 dark:divide-gray-800'
        $content = $content -replace 'hover:bg-gray-50 dark:hover:bg-gray-700', 'hover:bg-gray-100 dark:hover:bg-gray-950'
        $content = $content -replace 'bg-gray-50 dark:bg-gray-700/50', 'bg-gray-100 dark:bg-gray-950'
        
        if ($content -ne $original) {
            Set-Content -Path $file -Value $content -NoNewline
            $count++
            Write-Host "  Updated" -ForegroundColor Green
        } else {
            Write-Host "  No changes" -ForegroundColor Gray
        }
    }
}

Write-Host ""
Write-Host "Complete! Updated $count files." -ForegroundColor Cyan
