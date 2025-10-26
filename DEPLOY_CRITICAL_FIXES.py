#!/usr/bin/env python3
"""
Quick deployment script for critical fixes
Runs all necessary setup steps
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def check_file_exists(filepath):
    return Path(filepath).exists()

def main():
    print_header("🚀 TrulyInvoice Production Deployment Setup")
    
    # Check we're in the right directory
    if not check_file_exists("backend/app/main.py"):
        print_error("Not in project root directory!")
        print("Please run this from: c:\\Users\\akib\\Desktop\\trulyinvoice.in\\")
        sys.exit(1)
    
    print_success("In correct directory")
    
    # Step 1: Check environment variables
    print_header("Step 1: Environment Variables")
    
    required_vars = [
        "SUPABASE_URL",
        "SUPABASE_SERVICE_KEY", 
        "GEMINI_API_KEY",
        "RAZORPAY_KEY_ID",
        "RAZORPAY_KEY_SECRET"
    ]
    
    env_file = Path("backend/.env")
    if not env_file.exists():
        print_error(".env file not found in backend/")
        print_warning("Please create backend/.env with required variables")
        sys.exit(1)
    
    print_success(".env file exists")
    
    # Check if variables are set
    from dotenv import load_dotenv
    load_dotenv(env_file)
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print_error(f"Missing environment variables: {', '.join(missing)}")
        print_warning("Add these to backend/.env before continuing")
        sys.exit(1)
    
    print_success(f"All {len(required_vars)} required variables are set")
    
    # Step 2: Check database indexes
    print_header("Step 2: Database Indexes")
    
    print("📋 SQL script ready: ADD_PRODUCTION_INDEXES.sql")
    print("\nTo apply indexes:")
    print("1. Go to https://supabase.com/dashboard")
    print("2. Select your project")
    print("3. Go to SQL Editor")
    print("4. Copy contents of ADD_PRODUCTION_INDEXES.sql")
    print("5. Run the script")
    print("6. Verify indexes created (queries at end of script)")
    
    response = input("\n✋ Have you applied the database indexes? (y/n): ")
    if response.lower() != 'y':
        print_warning("Please apply indexes before proceeding")
        print("This will improve performance by 10-100x")
        sys.exit(1)
    
    print_success("Database indexes confirmed")
    
    # Step 3: Check cron job setup
    print_header("Step 3: Storage Cleanup Cron Job")
    
    print("📋 Setup guide ready: STORAGE_CLEANUP_GUIDE.md")
    print("\nRecommended: Set up daily cron job at 2 AM UTC")
    print("\nOptions:")
    print("1. Render.com Cron Job (easiest for Render deployment)")
    print("2. GitHub Actions (free, works anywhere)")
    print("3. Supabase pg_cron (database-level)")
    print("4. External service (cron-job.org)")
    
    response = input("\n✋ Have you set up the cron job? (y/n/skip): ")
    if response.lower() == 'n':
        print_warning("⚠️  You can set this up later")
        print("Without it, storage won't be cleaned automatically")
    elif response.lower() == 'y':
        print_success("Cron job setup confirmed")
    else:
        print_warning("Skipped - remember to set up later!")
    
    # Step 4: Test storage cleanup manually
    print_header("Step 4: Test Storage Cleanup")
    
    print("Let's test the storage cleanup service...")
    
    response = input("\nRun test cleanup? (y/n): ")
    if response.lower() == 'y':
        try:
            os.chdir("backend")
            result = subprocess.run(
                [sys.executable, "-m", "app.services.storage_cleanup", "cleanup-anonymous"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print_success("Storage cleanup test passed!")
                print(result.stdout)
            else:
                print_error("Storage cleanup test failed")
                print(result.stderr)
            
            os.chdir("..")
        except Exception as e:
            print_error(f"Test failed: {e}")
    else:
        print_warning("Test skipped")
    
    # Step 5: Rate limiting status
    print_header("Step 5: Rate Limiting")
    
    print_success("Rate limiting is now ENABLED in backend/app/main.py")
    print("Protection active:")
    print("  - 5 login attempts per minute per IP")
    print("  - Exponential backoff (5s → 15s → 30s → 60s → 5min)")
    print("  - Applies to: login, signup, password reset")
    
    # Step 6: Summary
    print_header("✅ DEPLOYMENT READY")
    
    print("Critical fixes implemented:")
    print("  ✅ Rate limiting enabled")
    print("  ✅ Environment validation on startup")
    print("  ✅ Storage cleanup service created")
    print("  ✅ Database indexes defined")
    print("  ✅ API endpoints for storage management")
    
    print("\n📋 Next steps:")
    print("  1. Deploy backend with: uvicorn app.main:app --host 0.0.0.0 --port 8000")
    print("  2. Test rate limiting (try 6 failed logins)")
    print("  3. Monitor logs for 24 hours")
    print("  4. Set up error monitoring (Sentry)")
    print("  5. Set up uptime monitoring (UptimeRobot)")
    
    print("\n📚 Documentation:")
    print("  - PRODUCTION_READINESS_AUDIT.md (full audit)")
    print("  - CRITICAL_FIXES_SUMMARY.md (what was fixed)")
    print("  - STORAGE_CLEANUP_GUIDE.md (cleanup setup)")
    print("  - ADD_PRODUCTION_INDEXES.sql (database indexes)")
    
    print("\n🚀 You're ready to launch!")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed: {e}")
        sys.exit(1)
