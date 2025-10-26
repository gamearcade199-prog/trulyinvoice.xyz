# Fix canonical URLs for all 20 city pages
# Changes from /invoice-software-[city] to /invoice-software/[city]

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
        $oldCanonical = "canonical: 'https://trulyinvoice.xyz/invoice-software-$city'"
        $newCanonical = "canonical: 'https://trulyinvoice.xyz/invoice-software/$city'"
        
        if ($content -match [regex]::Escape($oldCanonical)) {
            $content = $content -replace [regex]::Escape($oldCanonical), $newCanonical
            Set-Content -Path $filePath -Value $content -NoNewline
            Write-Host "✅ Fixed canonical for $city" -ForegroundColor Green
        } else {
            Write-Host "⚠️  $city already correct or not found" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ File not found: $filePath" -ForegroundColor Red
    }
}

Write-Host "`n✅ All city canonical URLs fixed!" -ForegroundColor Green
