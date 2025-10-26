# Remove fake phone numbers from all city pages

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
        
        # Remove telephone line
        $content = $content -replace "\s*'telephone':\s*'[^']*',?\s*", "`n    "
        
        Set-Content -Path $filePath -Value $content -NoNewline
        Write-Host "✅ Cleaned schema for $city" -ForegroundColor Green
    } else {
        Write-Host "❌ File not found: $filePath" -ForegroundColor Red
    }
}

Write-Host "`n✅ All placeholder data removed from city pages!" -ForegroundColor Green
