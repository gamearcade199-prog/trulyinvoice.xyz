#!/usr/bin/env pwsh
# Script to update all .xyz domain references to .com

Write-Host "🔄 Updating all trulyinvoice.xyz to trulyinvoice.com..." -ForegroundColor Cyan

# Define the directories to search
$directories = @(
    "frontend\src\app",
    "frontend\src\components",
    "frontend\src\lib",
    "frontend\src\config"
)

$totalFiles = 0
$totalReplacements = 0

foreach ($dir in $directories) {
    $path = Join-Path $PSScriptRoot $dir
    
    if (Test-Path $path) {
        Write-Host "`n📁 Processing directory: $dir" -ForegroundColor Yellow
        
        # Get all .tsx, .ts, .jsx, .js files
        $files = Get-ChildItem -Path $path -Recurse -Include "*.tsx", "*.ts", "*.jsx", "*.js" -File
        
        foreach ($file in $files) {
            $content = Get-Content $file.FullName -Raw
            
            # Check if file contains trulyinvoice.xyz
            if ($content -match "trulyinvoice\.xyz") {
                # Replace all instances
                $newContent = $content -replace "trulyinvoice\.xyz", "trulyinvoice.com"
                
                # Count replacements
                $matches = ([regex]::Matches($content, "trulyinvoice\.xyz")).Count
                
                # Write the new content
                Set-Content -Path $file.FullName -Value $newContent -NoNewline
                
                $totalFiles++
                $totalReplacements += $matches
                
                Write-Host "  ✅ Updated: $($file.Name) ($matches replacements)" -ForegroundColor Green
            }
        }
    } else {
        Write-Host "  ⚠️  Directory not found: $path" -ForegroundColor Red
    }
}

Write-Host "`n" -NoNewline
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✨ Domain Update Complete!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "📊 Files Updated: $totalFiles" -ForegroundColor Yellow
Write-Host "🔄 Total Replacements: $totalReplacements" -ForegroundColor Yellow
Write-Host "🎯 Old Domain: trulyinvoice.xyz" -ForegroundColor Red
Write-Host "🎯 New Domain: trulyinvoice.com" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan

Write-Host "`n✅ All SEO files updated to .com domain!" -ForegroundColor Green
Write-Host "🚀 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Run: cd frontend ; npm run build" -ForegroundColor White
Write-Host "   2. Test locally: npm run dev" -ForegroundColor White
Write-Host "   3. Commit changes: git add . && git commit -m 'Update domain to .com'" -ForegroundColor White
Write-Host "   4. Push to Vercel: git push" -ForegroundColor White
Write-Host "   5. Verify on: https://trulyinvoice.com" -ForegroundColor White
