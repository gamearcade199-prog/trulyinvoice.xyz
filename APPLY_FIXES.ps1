# QUICK FIX SCRIPT - Critical Issues Resolution
# Run this to fix the most critical issues found in beta testing

Write-Host "=================================================================="
Write-Host "TRULYINVOICE.XYZ - CRITICAL FIXES AUTOMATION"
Write-Host "=================================================================="
Write-Host ""

$ErrorActionPreference = "Continue"
$FixesApplied = 0
$FixesFailed = 0

# FIX 1: Install Missing NPM Packages
Write-Host "[FIX 1] Installing Missing NPM Packages"
Write-Host "----------------------------------------------------------------"

try {
    Set-Location "$PSScriptRoot\frontend"
    Write-Host "Installing react-hot-toast..."
    npm install react-hot-toast --silent
    
    Write-Host "Installing @headlessui/react..."
    npm install @headlessui/react --silent
    
    Write-Host "[SUCCESS] NPM packages installed"
    $FixesApplied++
}
catch {
    Write-Host "[FAILED] Could not install NPM packages: $_"
    $FixesFailed++
}

# FIX 2: Create Backend __init__.py
Write-Host ""
Write-Host "[FIX 2] Creating Backend __init__.py"
Write-Host "----------------------------------------------------------------"

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
    Write-Host "[SUCCESS] Created backend/__init__.py"
    $FixesApplied++
}
catch {
    Write-Host "[FAILED] Could not create __init__.py: $_"
    $FixesFailed++
}

# FIX 3: Create Supabase Client Wrapper
Write-Host ""
Write-Host "[FIX 3] Creating Supabase Client Wrappers"
Write-Host "----------------------------------------------------------------"

try {
    $supabaseDir = "$PSScriptRoot\frontend\src\lib\supabase"
    
    if (-not (Test-Path $supabaseDir)) {
        New-Item -ItemType Directory -Path $supabaseDir -Force | Out-Null
        Write-Host "Created directory: src/lib/supabase"
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
    Write-Host "[SUCCESS] Created src/lib/supabase/client.ts"
    
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
    Write-Host "[SUCCESS] Created src/lib/supabase/server.ts"
    
    $FixesApplied++
}
catch {
    Write-Host "[FAILED] Could not create Supabase wrappers: $_"
    $FixesFailed++
}

# FIX 4: Install @supabase/ssr
Write-Host ""
Write-Host "[FIX 4] Installing @supabase/ssr"
Write-Host "----------------------------------------------------------------"

try {
    Set-Location "$PSScriptRoot\frontend"
    Write-Host "Installing @supabase/ssr..."
    npm install @supabase/ssr --silent
    
    Write-Host "[SUCCESS] @supabase/ssr installed"
    $FixesApplied++
}
catch {
    Write-Host "[FAILED] Could not install @supabase/ssr: $_"
    $FixesFailed++
}

# SUMMARY
Write-Host ""
Write-Host "=================================================================="
Write-Host "QUICK FIX SUMMARY"
Write-Host "=================================================================="
Write-Host ""
Write-Host "Fixes Applied: $FixesApplied"
Write-Host "Fixes Failed: $FixesFailed"
Write-Host ""

if ($FixesFailed -eq 0) {
    Write-Host "SUCCESS: ALL CRITICAL FIXES APPLIED!"
    Write-Host ""
    Write-Host "Next Steps:"
    Write-Host "1. Replace alert() calls with modal system"
    Write-Host "2. Run manual feature testing"
    Write-Host "3. Test payment flow end-to-end"
    Write-Host "4. Rotate API keys before production"
}
else {
    Write-Host "WARNING: SOME FIXES FAILED - CHECK ERRORS ABOVE"
}

Write-Host ""
Set-Location $PSScriptRoot
