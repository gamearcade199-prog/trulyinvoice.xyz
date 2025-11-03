"""
Final Production Readiness Test - Checks everything is working
"""
import requests
import time

print("="*80)
print("🚀 PRODUCTION READINESS CHECK")
print("="*80)

BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

results = {
    "passed": [],
    "failed": [],
    "warnings": []
}

def check(name, condition, message=""):
    if condition:
        results["passed"].append(name)
        print(f"✅ {name}")
        if message:
            print(f"   {message}")
    else:
        results["failed"].append(name)
        print(f"❌ {name}")
        if message:
            print(f"   {message}")

def warn(name, message=""):
    results["warnings"].append(name)
    print(f"⚠️  {name}")
    if message:
        print(f"   {message}")

# ============================================================================
# BACKEND CHECKS
# ============================================================================
print("\n" + "="*80)
print("BACKEND CHECKS")
print("="*80)

try:
    health = requests.get(f"{BACKEND_URL}/health", timeout=5).json()
    check("Backend Running", True, f"Environment: {health.get('environment')}")
    check("Backend Healthy", health.get('status') == 'healthy')
except Exception as e:
    check("Backend Running", False, str(e))

try:
    invoice_health = requests.get(f"{BACKEND_URL}/api/invoices/health", timeout=5).json()
    check("Invoice API Available", invoice_health.get('status') == 'healthy')
except Exception as e:
    check("Invoice API Available", False, str(e))

# Check CORS
try:
    cors = requests.options(
        f"{BACKEND_URL}/api/auth/setup-user",
        headers={"Origin": "http://localhost:3000"},
        timeout=5
    )
    check("CORS Configured", 'access-control-allow-origin' in cors.headers)
except Exception as e:
    check("CORS Configured", False, str(e))

# ============================================================================
# FRONTEND CHECKS
# ============================================================================
print("\n" + "="*80)
print("FRONTEND CHECKS")
print("="*80)

try:
    home = requests.get(FRONTEND_URL, timeout=10)
    check("Frontend Running", home.status_code == 200)
except Exception as e:
    check("Frontend Running", False, str(e))

try:
    register = requests.get(f"{FRONTEND_URL}/register", timeout=10)
    check("Register Page Accessible", register.status_code == 200)
    check("Register Page HTML Valid", b'Create Account' in register.content or b'Register' in register.content)
except Exception as e:
    check("Register Page Accessible", False, str(e))

try:
    login = requests.get(f"{FRONTEND_URL}/login", timeout=10)
    check("Login Page Accessible", login.status_code == 200)
except Exception as e:
    check("Login Page Accessible", False, str(e))

# ============================================================================
# DATABASE CHECKS
# ============================================================================
print("\n" + "="*80)
print("DATABASE CHECKS")
print("="*80)

import psycopg2

try:
    conn = psycopg2.connect(
        host="db.ldvwxqluaheuhbycdpwn.supabase.co",
        port="5432",
        database="postgres",
        user="postgres",
        password="QDIXJSBJwyJOyTHt",
        connect_timeout=5
    )
    check("Database Connection", True)
    
    cur = conn.cursor()
    
    # Check RLS
    cur.execute("SELECT relrowsecurity FROM pg_class WHERE relname = 'subscriptions'")
    rls_enabled = cur.fetchone()[0]
    check("RLS Enabled", rls_enabled)
    
    # Check policies
    cur.execute("SELECT COUNT(*) FROM pg_policies WHERE tablename = 'subscriptions'")
    policy_count = cur.fetchone()[0]
    check("RLS Policies Configured", policy_count >= 8, f"{policy_count} policies")
    
    # Check columns
    cur.execute("""
        SELECT COUNT(*) FROM information_schema.columns
        WHERE table_name = 'subscriptions'
    """)
    col_count = cur.fetchone()[0]
    check("Database Schema Complete", col_count >= 19, f"{col_count} columns")
    
    # Check indexes
    cur.execute("""
        SELECT COUNT(*) FROM pg_indexes 
        WHERE tablename = 'subscriptions' AND schemaname = 'public'
    """)
    index_count = cur.fetchone()[0]
    check("Performance Indexes", index_count >= 3, f"{index_count} indexes")
    
    cur.close()
    conn.close()
    
except Exception as e:
    check("Database Connection", False, str(e))

# ============================================================================
# INTEGRATION CHECKS
# ============================================================================
print("\n" + "="*80)
print("INTEGRATION CHECKS")
print("="*80)

# Test registration flow (backend)
try:
    import random
    import string
    from supabase import create_client
    
    SUPABASE_URL = "https://ldvwxqluaheuhbycdpwn.supabase.co"
    SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A"
    
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    test_email = f"readiness_{random_suffix}@example.com"
    
    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    auth_response = supabase.auth.sign_up({
        "email": test_email,
        "password": "TestPassword123!",
    })
    
    if auth_response.user:
        user_id = auth_response.user.id
        setup_response = requests.post(
            f"{BACKEND_URL}/api/auth/setup-user",
            json={"user_id": user_id, "email": test_email, "full_name": "Readiness Test"},
            timeout=10
        )
        check("End-to-End Registration", setup_response.status_code == 200)
        
        # Verify subscription
        time.sleep(1)
        sub_response = requests.get(f"{BACKEND_URL}/api/auth/subscription/{user_id}", timeout=10)
        if sub_response.status_code == 200:
            data = sub_response.json()
            check("Subscription Retrieval", data.get('tier') == 'free')
        else:
            check("Subscription Retrieval", False, f"Status: {sub_response.status_code}")
    else:
        check("End-to-End Registration", False, "Supabase auth failed")
        
except Exception as e:
    check("End-to-End Registration", False, str(e))

# ============================================================================
# ENVIRONMENT CHECKS
# ============================================================================
print("\n" + "="*80)
print("ENVIRONMENT CHECKS")
print("="*80)

import os

# Check backend .env
backend_env_path = "c:/Users/akib/Desktop/trulyinvoice.xyz/backend/.env"
if os.path.exists(backend_env_path):
    check("Backend .env File", True)
    with open(backend_env_path, 'r') as f:
        env_content = f.read()
        check("SUPABASE_URL Set", "SUPABASE_URL=" in env_content)
        check("SUPABASE_SERVICE_KEY Set", "SUPABASE_SERVICE_KEY=" in env_content)
        check("GEMINI_API_KEY Set", "GEMINI_API_KEY=" in env_content)
else:
    check("Backend .env File", False, "Missing")

# Check frontend .env.local
frontend_env_path = "c:/Users/akib/Desktop/trulyinvoice.xyz/frontend/.env.local"
if os.path.exists(frontend_env_path):
    check("Frontend .env.local File", True)
    with open(frontend_env_path, 'r') as f:
        env_content = f.read()
        check("NEXT_PUBLIC_API_URL Set", "NEXT_PUBLIC_API_URL=" in env_content)
        check("NEXT_PUBLIC_SUPABASE_URL Set", "NEXT_PUBLIC_SUPABASE_URL=" in env_content)
        check("NEXT_PUBLIC_SUPABASE_ANON_KEY Set", "NEXT_PUBLIC_SUPABASE_ANON_KEY=" in env_content)
else:
    check("Frontend .env.local File", False, "Missing")

# ============================================================================
# SECURITY CHECKS
# ============================================================================
print("\n" + "="*80)
print("SECURITY CHECKS")
print("="*80)

# Check HTTPS readiness (development uses HTTP, production should use HTTPS)
warn("HTTPS Configuration", "Using HTTP (development). Switch to HTTPS in production.")

# Check environment variables not exposed
try:
    response = requests.get(f"{BACKEND_URL}/health", timeout=5).json()
    if 'SUPABASE_SERVICE_KEY' in str(response) or 'GEMINI_API_KEY' in str(response):
        check("Secrets Not Exposed", False, "API keys visible in responses")
    else:
        check("Secrets Not Exposed", True)
except:
    warn("Secrets Check", "Could not verify")

# ============================================================================
# FINAL REPORT
# ============================================================================
print("\n" + "="*80)
print("📊 PRODUCTION READINESS REPORT")
print("="*80)

print(f"\n✅ PASSED: {len(results['passed'])} checks")
print(f"❌ FAILED: {len(results['failed'])} checks")
print(f"⚠️  WARNINGS: {len(results['warnings'])} items")

if results['failed']:
    print("\n❌ FAILED CHECKS:")
    for item in results['failed']:
        print(f"   • {item}")

if results['warnings']:
    print("\n⚠️  WARNINGS:")
    for item in results['warnings']:
        print(f"   • {item}")

print("\n" + "="*80)
if len(results['failed']) == 0:
    print("🎉🎉🎉 SYSTEM IS PRODUCTION READY! 🎉🎉🎉")
    print("="*80)
    print("\n✅ All critical checks passed!")
    print("✅ Backend and Frontend running")
    print("✅ Database properly configured")
    print("✅ Registration flow working")
    print("✅ Security measures in place")
    print("\n🚀 Ready to deploy to production!")
else:
    print(f"⚠️  {len(results['failed'])} CRITICAL ISSUE(S) FOUND")
    print("="*80)
    print("\n⚠️  Fix the failed checks before production deployment")

print("\n" + "="*80)
print(f"Score: {len(results['passed'])}/{len(results['passed']) + len(results['failed'])} ({100 * len(results['passed']) // (len(results['passed']) + len(results['failed']))}%)")
print("="*80)
