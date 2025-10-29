# 🚀 QUICK FIX SCRIPT - Critical Issues Resolution
# Run this to fix the most critical issues found in beta testing

Write-Host "=" -NoNewline -ForegroundColor Cyan; Write-Host "="*79 -ForegroundColor Cyan
Write-Host "🔧 TRULYINVOICE.XYZ - CRITICAL FIXES AUTOMATION" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan; Write-Host "="*79 -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Continue"
$FixesApplied = 0
$FixesFailed = 0

# ============================================================================
# FIX 1: Install Missing NPM Packages
# ============================================================================
Write-Host "📦 FIX 1: Installing Missing NPM Packages" -ForegroundColor Cyan
Write-Host "-"*80 -ForegroundColor DarkGray

try {
    Set-Location "$PSScriptRoot\frontend"
    Write-Host "Installing react-hot-toast..." -ForegroundColor Yellow
    npm install react-hot-toast
    
    Write-Host "Installing @headlessui/react..." -ForegroundColor Yellow
    npm install @headlessui/react
    
    Write-Host "✅ NPM packages installed successfully" -ForegroundColor Green
    $FixesApplied++
}
catch {
    Write-Host "❌ Failed to install NPM packages: $_" -ForegroundColor Red
    $FixesFailed++
}

# ============================================================================
# FIX 2: Create Backend __init__.py
# ============================================================================
Write-Host ""
Write-Host "📦 FIX 2: Creating Backend __init__.py" -ForegroundColor Cyan
Write-Host "-"*80 -ForegroundColor DarkGray

try {
    $initPath = "$PSScriptRoot\backend\__init__.py"
    $initContent = @"
"""
TrulyInvoice Backend
AI-powered invoice processing system
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "TrulyInvoice Team"
"@
    
    Set-Content -Path $initPath -Value $initContent
    Write-Host "✅ Created backend/__init__.py" -ForegroundColor Green
    $FixesApplied++
}
catch {
    Write-Host "❌ Failed to create __init__.py: $_" -ForegroundColor Red
    $FixesFailed++
}

# ============================================================================
# FIX 3: Create Supabase Client Wrapper
# ============================================================================
Write-Host ""
Write-Host "📦 FIX 3: Creating Supabase Client Wrappers" -ForegroundColor Cyan
Write-Host "-"*80 -ForegroundColor DarkGray

try {
    $supabaseDir = "$PSScriptRoot\frontend\src\lib\supabase"
    
    # Create directory if it doesn't exist
    if (-not (Test-Path $supabaseDir)) {
        New-Item -ItemType Directory -Path $supabaseDir -Force | Out-Null
        Write-Host "Created directory: src/lib/supabase" -ForegroundColor Yellow
    }
    
    # Create client.ts
    $clientContent = @"
/**
 * Supabase Client (Browser-side)
 * For use in client components and browser context
 */
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables')
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
    detectSessionInUrl: true,
    storageKey: 'trulyinvoice-auth',
  },
})
"@
    
    Set-Content -Path "$supabaseDir\client.ts" -Value $clientContent
    Write-Host "✅ Created src/lib/supabase/client.ts" -ForegroundColor Green
    
    # Create server.ts
    $serverContent = @"
/**
 * Supabase Server Client
 * For use in server components, API routes, and server actions
 */
import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { cookies } from 'next/headers'

export function createClient() {
  const cookieStore = cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value
        },
        set(name: string, value: string, options: CookieOptions) {
          try {
            cookieStore.set({ name, value, ...options })
          } catch (error) {
            // Handle error when setting cookies in Server Components
          }
        },
        remove(name: string, options: CookieOptions) {
          try {
            cookieStore.set({ name, value: '', ...options })
          } catch (error) {
            // Handle error when removing cookies in Server Components
          }
        },
      },
    }
  )
}
"@
    
    Set-Content -Path "$supabaseDir\server.ts" -Value $serverContent
    Write-Host "✅ Created src/lib/supabase/server.ts" -ForegroundColor Green
    
    $FixesApplied++
}
catch {
    Write-Host "❌ Failed to create Supabase wrappers: $_" -ForegroundColor Red
    $FixesFailed++
}

# ============================================================================
# FIX 4: Update .env.example
# ============================================================================
Write-Host ""
Write-Host "📦 FIX 4: Updating .env.example" -ForegroundColor Cyan
Write-Host "-"*80 -ForegroundColor DarkGray

try {
    $envExamplePath = "$PSScriptRoot\frontend\.env.example"
    
    # Read existing content
    $existingContent = ""
    if (Test-Path $envExamplePath) {
        $existingContent = Get-Content $envExamplePath -Raw
    }
    
    # Check what's missing and add it
    $missingVars = @()
    
    if ($existingContent -notmatch "NEXT_PUBLIC_SUPABASE_URL") {
        $missingVars += @"

# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
"@
    }
    
    if ($existingContent -notmatch "NEXT_PUBLIC_SUPABASE_ANON_KEY") {
        $missingVars += "NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key_here"
    }
    
    if ($existingContent -notmatch "NEXT_PUBLIC_RAZORPAY_KEY_ID") {
        $missingVars += @"

# Payment Gateway
NEXT_PUBLIC_RAZORPAY_KEY_ID=rzp_test_your_key_here
"@
    }
    
    if ($missingVars.Count -gt 0) {
        $updatedContent = $existingContent + "`n" + ($missingVars -join "`n")
        Set-Content -Path $envExamplePath -Value $updatedContent
        Write-Host "✅ Updated .env.example with missing variables" -ForegroundColor Green
        $FixesApplied++
    }
    else {
        Write-Host "✅ .env.example already complete" -ForegroundColor Green
        $FixesApplied++
    }
}
catch {
    Write-Host "❌ Failed to update .env.example: $_" -ForegroundColor Red
    $FixesFailed++
}

# ============================================================================
# FIX 5: Install @supabase/ssr (required for server client)
# ============================================================================
Write-Host ""
Write-Host "📦 FIX 5: Installing @supabase/ssr" -ForegroundColor Cyan
Write-Host "-"*80 -ForegroundColor DarkGray

try {
    Set-Location "$PSScriptRoot\frontend"
    Write-Host "Installing @supabase/ssr..." -ForegroundColor Yellow
    npm install @supabase/ssr
    
    Write-Host "✅ @supabase/ssr installed successfully" -ForegroundColor Green
    $FixesApplied++
}
catch {
    Write-Host "❌ Failed to install @supabase/ssr: $_" -ForegroundColor Red
    $FixesFailed++
}

# ============================================================================
# SUMMARY
# ============================================================================
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan; Write-Host "="*79 -ForegroundColor Cyan
Write-Host "📊 QUICK FIX SUMMARY" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan; Write-Host "="*79 -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Fixes Applied: $FixesApplied" -ForegroundColor Green
Write-Host "❌ Fixes Failed: $FixesFailed" -ForegroundColor Red
Write-Host ""

if ($FixesFailed -eq 0) {
    Write-Host "🎉 ALL CRITICAL FIXES APPLIED SUCCESSFULLY!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Replace alert() calls with modal system (see COMPREHENSIVE_BETA_TEST_REPORT.md)" -ForegroundColor White
    Write-Host "2. Run manual feature testing" -ForegroundColor White
    Write-Host "3. Test payment flow end-to-end" -ForegroundColor White
    Write-Host "4. Verify rate limiting with real requests" -ForegroundColor White
    Write-Host "5. Rotate API keys before production deployment" -ForegroundColor White
}
else {
    Write-Host "⚠️  SOME FIXES FAILED - CHECK ERRORS ABOVE" -ForegroundColor Red
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan; Write-Host "="*79 -ForegroundColor Cyan
Write-Host ""

# Return to original directory
Set-Location $PSScriptRoot
