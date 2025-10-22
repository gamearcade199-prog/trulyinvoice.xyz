# Remove fake aggregateRating from all city pages

$cities = @(
    "mumbai", "delhi", "bangalore", "chennai", "kolkata", "hyderabad",
    "pune", "ahmedabad", "jaipur", "lucknow", "kanpur", "nagpur",
    "indore", "thane", "bhopal", "visakhapatnam", "pimpri-chinchwad",
    "patna", "vadodara", "surat"
)

foreach ($city in $cities) {
    $filePath = "frontend\src\app\invoice-software\$city\page.tsx"
    
    if (Test-Path $filePath) {
        $content = Get-Content $filePath -Raw
        
        # Remove aggregateRating section
        $pattern = ",\s*'aggregateRating':\s*\{[^\}]*\}"
        if ($content -match $pattern) {
            $content = $content -replace $pattern, ""
            Set-Content -Path $filePath -Value $content -NoNewline
            Write-Host "✅ Removed fake rating from $city" -ForegroundColor Green
        } else {
            Write-Host "⚠️  No rating found in $city or already removed" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ File not found: $filePath" -ForegroundColor Red
    }
}

Write-Host "`n✅ All fake ratings removed from city pages!" -ForegroundColor Green
