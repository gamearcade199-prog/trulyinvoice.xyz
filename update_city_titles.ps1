# Update meta titles to match new H1s

$cities = @(
    "mumbai", "delhi", "bangalore", "chennai", "kolkata", "hyderabad",
    "pune", "ahmedabad", "jaipur", "lucknow", "kanpur", "nagpur",
    "indore", "thane", "bhopal", "visakhapatnam", "pimpri-chinchwad",
    "patna", "vadodara", "surat"
)

$cityNames = @{
    "mumbai" = "Mumbai"
    "delhi" = "Delhi"
    "bangalore" = "Bangalore"
    "chennai" = "Chennai"
    "kolkata" = "Kolkata"
    "hyderabad" = "Hyderabad"
    "pune" = "Pune"
    "ahmedabad" = "Ahmedabad"
    "jaipur" = "Jaipur"
    "lucknow" = "Lucknow"
    "kanpur" = "Kanpur"
    "nagpur" = "Nagpur"
    "indore" = "Indore"
    "thane" = "Thane"
    "bhopal" = "Bhopal"
    "visakhapatnam" = "Visakhapatnam"
    "pimpri-chinchwad" = "Pimpri-Chinchwad"
    "patna" = "Patna"
    "vadodara" = "Vadodara"
    "surat" = "Surat"
}

foreach ($city in $cities) {
    $filePath = "frontend\src\app\invoice-software\$city\page.tsx"
    $cityName = $cityNames[$city]
    
    if (Test-Path $filePath) {
        $content = Get-Content $filePath -Raw
        
        # Update meta title to match H1
        $oldTitle = "Invoice Management Software $cityName | GST & AI | TrulyInvoice"
        $newTitle = "Invoice to Excel Software $cityName | AI-Powered GST Converter"
        
        if ($content -match [regex]::Escape($oldTitle)) {
            $content = $content -replace [regex]::Escape($oldTitle), $newTitle
            Set-Content -Path $filePath -Value $content -NoNewline
            Write-Host "✅ Updated title for $cityName" -ForegroundColor Green
        } else {
            Write-Host "⚠️  $cityName title not found or already updated" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ File not found: $filePath" -ForegroundColor Red
    }
}

Write-Host "`n✅ All city page titles now match H1s!" -ForegroundColor Green
