# Start backend with API keys - FOR POWERSHELL
# This ensures environment variables are loaded before Python starts

Set-Location $PSScriptRoot

# Set API Keys (replace with your actual keys)
$env:GOOGLE_AI_API_KEY = "YOUR_GOOGLE_AI_API_KEY_HERE"
$env:GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# Also set other important vars
$env:SUPABASE_URL = "https://ldvwxqluaheuhbycdpwn.supabase.co"
$env:SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDA3NjY1NiwiZXhwIjoyMDc1NjUyNjU2fQ.939ySYuwA9ByCprCiI9GL5xEmvkhONYEWdtuHVLweWM"

Write-Host "✅ Environment variables set" -ForegroundColor Green
Write-Host "   - GOOGLE_AI_API_KEY: Set" 
Write-Host "   - GEMINI_API_KEY: Set"
Write-Host "   - SUPABASE_URL: Set"
Write-Host "   - SUPABASE_SERVICE_KEY: Set"
Write-Host ""

# Activate venv
.\venv\Scripts\Activate.ps1

# Start backend
Write-Host "🚀 Starting backend on port 8000..." -ForegroundColor Cyan
python -m uvicorn app.main:app --reload --port 8000 --log-level info

Read-Host "Press Enter to exit"
