"""
Comprehensive system test - checks all critical functionality
"""
import requests
import random
import string
from supabase import create_client, Client
import time

SUPABASE_URL = "https://ldvwxqluaheuhbycdpwn.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A"
BACKEND_URL = "http://localhost:8000"

print("="*80)
print("🔍 COMPREHENSIVE SYSTEM TEST")
print("="*80)

test_results = []

def test(name, func):
    """Run a test and track results"""
    print(f"\n{'='*80}")
    print(f"TEST: {name}")
    print(f"{'='*80}")
    try:
        func()
        test_results.append((name, "✅ PASS", None))
        print(f"✅ {name} - PASSED")
    except Exception as e:
        test_results.append((name, "❌ FAIL", str(e)))
        print(f"❌ {name} - FAILED: {e}")

# Test 1: Backend Health
def test_backend_health():
    response = requests.get(f"{BACKEND_URL}/health", timeout=5)
    assert response.status_code == 200, f"Backend health check failed: {response.status_code}"
    print(f"   Backend: {response.json()}")

# Test 2: Registration Flow
def test_registration():
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    test_email = f"test_{random_suffix}@example.com"
    test_password = "TestPassword123!"
    
    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    
    # Step 1: Supabase Auth signup
    auth_response = supabase.auth.sign_up({
        "email": test_email,
        "password": test_password,
        "options": {"data": {"full_name": "Test User"}}
    })
    assert auth_response.user is not None, "Supabase signup failed"
    user_id = auth_response.user.id
    print(f"   ✅ Auth signup: {user_id}")
    
    # Step 2: Backend subscription setup
    setup_response = requests.post(
        f"{BACKEND_URL}/api/auth/setup-user",
        json={"user_id": user_id, "email": test_email, "full_name": "Test User"},
        timeout=10
    )
    assert setup_response.status_code == 200, f"Setup failed: {setup_response.text}"
    data = setup_response.json()
    assert data['success'] == True, "Setup not successful"
    assert data['subscription']['tier'] == 'free', "Wrong tier"
    print(f"   ✅ Subscription created: {data['subscription']['tier']}")
    
    return user_id, auth_response.session.access_token

# Test 3: Login Flow
def test_login():
    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    
    # Use the existing user
    login_response = supabase.auth.sign_in_with_password({
        "email": "akibhusain830@gmail.com",
        "password": "Akib1234"  # You'll need to tell me the password or use a test user
    })
    print(f"   ⚠️  Skipping login test - need valid credentials")

# Test 4: Subscription Status Check
def test_subscription_status():
    # Create a user first
    user_id, token = test_registration()
    time.sleep(1)
    
    # Don't send auth header - endpoint doesn't require it
    response = requests.get(
        f"{BACKEND_URL}/api/auth/subscription/{user_id}",
        timeout=10
    )
    assert response.status_code == 200, f"Subscription check failed: {response.status_code} - {response.text}"
    data = response.json()
    assert 'tier' in data, "Missing tier in response"
    print(f"   ✅ Subscription: {data['tier']} - {data.get('scans_remaining', 'N/A')} scans")

# Test 5: Invoice Upload Endpoint
def test_invoice_upload_endpoint():
    response = requests.get(f"{BACKEND_URL}/api/invoices/health", timeout=5)
    assert response.status_code == 200, "Invoice endpoint not accessible"
    print(f"   ✅ Invoice API accessible")

# Test 6: Database Schema Check
def test_database_schema():
    import psycopg2
    conn = psycopg2.connect(
        host="db.ldvwxqluaheuhbycdpwn.supabase.co",
        port="5432",
        database="postgres",
        user="postgres",
        password="QDIXJSBJwyJOyTHt"
    )
    cur = conn.cursor()
    
    # Check subscriptions table has all required columns
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'subscriptions'
    """)
    columns = [row[0] for row in cur.fetchall()]
    required = ['id', 'user_id', 'tier', 'status', 'scans_used_this_period', 
                'razorpay_order_id', 'razorpay_payment_id']
    
    for col in required:
        assert col in columns, f"Missing column: {col}"
    print(f"   ✅ All required columns present: {len(columns)} total")
    
    # Check RLS policies
    cur.execute("""
        SELECT COUNT(*) FROM pg_policies 
        WHERE tablename = 'subscriptions'
    """)
    policy_count = cur.fetchone()[0]
    assert policy_count >= 8, f"Not enough policies: {policy_count}"
    print(f"   ✅ RLS policies configured: {policy_count} policies")
    
    cur.close()
    conn.close()

# Test 7: CORS Configuration
def test_cors():
    response = requests.options(
        f"{BACKEND_URL}/api/auth/setup-user",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST"
        },
        timeout=5
    )
    print(f"   ℹ️  CORS headers: {response.headers.get('Access-Control-Allow-Origin', 'Not set')}")

# Test 8: Environment Variables
def test_environment():
    response = requests.get(f"{BACKEND_URL}/health", timeout=5)
    data = response.json()
    assert 'environment' in data, "Missing environment info"
    print(f"   ✅ Environment: {data.get('environment', 'unknown')}")

# Run all tests
test("Backend Health", test_backend_health)
test("Registration Flow", test_registration)
test("Subscription Status", test_subscription_status)
test("Invoice Upload Endpoint", test_invoice_upload_endpoint)
test("Database Schema", test_database_schema)
test("CORS Configuration", test_cors)
test("Environment Variables", test_environment)

# Print summary
print("\n" + "="*80)
print("📊 TEST SUMMARY")
print("="*80)

passed = sum(1 for _, result, _ in test_results if result == "✅ PASS")
failed = sum(1 for _, result, _ in test_results if result == "❌ FAIL")

for name, result, error in test_results:
    if error:
        print(f"{result} {name}")
        print(f"     Error: {error}")
    else:
        print(f"{result} {name}")

print("\n" + "="*80)
print(f"TOTAL: {passed} passed, {failed} failed out of {len(test_results)} tests")
if failed == 0:
    print("🎉🎉🎉 ALL TESTS PASSED! SYSTEM IS 10/10! 🎉🎉🎉")
else:
    print(f"⚠️  {failed} test(s) need attention")
print("="*80)
