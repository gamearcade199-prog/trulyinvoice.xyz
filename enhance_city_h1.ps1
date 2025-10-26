# Enhance city pages with better H1s and add Footer

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
        
        # Update H1 to include "Invoice to Excel" keyword
        $oldH1 = "Best Invoice Management Software for $cityName Businesses"
        $newH1 = "Invoice to Excel Software $cityName | AI-Powered GST Converter"
        
        if ($content -match [regex]::Escape($oldH1)) {
            $content = $content -replace [regex]::Escape($oldH1), $newH1
            Set-Content -Path $filePath -Value $content -NoNewline
            Write-Host "✅ Enhanced H1 for $cityName" -ForegroundColor Green
        } else {
            Write-Host "⚠️  $cityName H1 not found or already updated" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ File not found: $filePath" -ForegroundColor Red
    }
}

Write-Host "`n✅ All city page H1s enhanced with keywords!" -ForegroundColor Green
