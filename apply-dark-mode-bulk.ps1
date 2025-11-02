# Bulk Dark Mode Application Script
$file1 = "frontend\src\app\blog\how-to-extract-data-from-gst-invoices\page.tsx"
$file2 = "frontend\src\app\blog\bulk-csv-export-for-accounting-software\page.tsx"

$patterns = @{
    'className="bg-white rounded' = 'className="bg-white dark:bg-gray-800 rounded'
    'className="bg-white shadow' = 'className="bg-white dark:bg-gray-800 shadow'
    'className="bg-gray-50 rounded' = 'className="bg-gray-50 dark:bg-gray-900 rounded'
    'className="bg-blue-50 rounded' = 'className="bg-blue-50 dark:bg-blue-900/20 rounded'
    'className="bg-blue-50 border' = 'className="bg-blue-50 dark:bg-blue-900/20 border'
    'className="bg-green-50 rounded' = 'className="bg-green-50 dark:bg-green-900/20 rounded'
    'className="bg-red-50 rounded' = 'className="bg-red-50 dark:bg-red-900/20 rounded'
    'border-gray-200 ' = 'border-gray-200 dark:border-gray-700 '
    'border-blue-200 ' = 'border-blue-200 dark:border-blue-700 '
    'border-green-200 ' = 'border-green-200 dark:border-green-700 '
    'border-red-200 ' = 'border-red-200 dark:border-red-700 '
    'text-gray-900 mb' = 'text-gray-900 dark:text-white mb'
    'text-gray-700 mb' = 'text-gray-700 dark:text-gray-300 mb'
    'text-gray-700">' = 'text-gray-700 dark:text-gray-300">'
    'text-gray-700 space' = 'text-gray-700 dark:text-gray-300 space'
    'text-gray-600 mb' = 'text-gray-600 dark:text-gray-400 mb'
    'text-gray-600">' = 'text-gray-600 dark:text-gray-400">'
    'text-blue-900 mb' = 'text-blue-900 dark:text-blue-200 mb'
    'text-blue-900">' = 'text-blue-900 dark:text-blue-200">'
    'text-blue-800 ' = 'text-blue-800 dark:text-blue-300 '
    'text-blue-600 hover' = 'text-blue-600 dark:text-blue-400 hover'
    'text-green-900 mb' = 'text-green-900 dark:text-green-200 mb'
    'text-green-900">' = 'text-green-900 dark:text-green-200">'
    'text-green-800 ' = 'text-green-800 dark:text-green-300 '
    'text-red-900 mb' = 'text-red-900 dark:text-red-200 mb'
    'text-red-900">' = 'text-red-900 dark:text-red-200">'
    'text-red-800 ' = 'text-red-800 dark:text-red-300 '
    'text-purple-900 mb' = 'text-purple-900 dark:text-purple-200 mb'
    'hover:text-blue-600' = 'hover:text-blue-600 dark:hover:text-blue-400'
}

foreach ($file in @($file1, $file2)) {
    Write-Host "Processing $file..." -ForegroundColor Cyan
    $content = Get-Content $file -Raw
    $changeCount = 0
    
    foreach ($key in $patterns.Keys) {
        $value = $patterns[$key]
        if ($content -match [regex]::Escape($key)) {
            $content = $content.Replace($key, $value)
            $changeCount++
        }
    }
    
    Set-Content $file -Value $content -NoNewline
    Write-Host "Completed $file - $changeCount pattern changes" -ForegroundColor Green
}

Write-Host "`n🎉 Dark mode applied to both articles!" -ForegroundColor Green
