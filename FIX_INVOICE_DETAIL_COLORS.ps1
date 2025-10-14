$file = "C:\Users\akib\Desktop\trulyinvoice.in\frontend\src\app\invoices\[id]\page.tsx"
$content = Get-Content -Path $file -Raw

# Update text colors for dark mode
$content = $content -replace 'text-gray-700 mb-2">', 'text-gray-700 dark:text-gray-300 mb-2">'
$content = $content -replace 'className="text-gray-600"', 'className="text-gray-600 dark:text-gray-400"'
$content = $content -replace 'text-gray-900">', 'text-gray-900 dark:text-white">'

Set-Content -Path $file -Value $content
Write-Host "Updated dark mode text colors" -ForegroundColor Green
