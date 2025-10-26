"""
Temporary test script to verify export endpoints work
"""
import requests
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Get a test token - use one from localStorage or Supabase Auth session
# For now, let's just test the endpoints exist

BASE_URL = "http://localhost:8000"

print("Testing Export Endpoints...")
print("=" * 60)

# Test 1: Check if backend is running
print("\n1️⃣ Checking if backend is running...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"   ✅ Backend is running (status: {response.status_code})")
except Exception as e:
    print(f"   ❌ Backend is not responding: {e}")
    exit(1)

# Test 2: Check if export endpoints exist (without auth)
print("\n2️⃣ Checking export endpoints...")
for endpoint in ['export-pdf', 'export-excel', 'export-csv']:
    try:
        response = requests.get(f"{BASE_URL}/api/invoices/test-id/{endpoint}", timeout=5)
        print(f"   📄 {endpoint}: Status {response.status_code}")
        if response.status_code == 401:
            print(f"      ℹ️  Returns 401 (expected - requires auth)")
        elif response.status_code == 404:
            print(f"      ℹ️  Returns 404 (invoice not found, but endpoint exists)")
    except Exception as e:
        print(f"   ❌ {endpoint}: {e}")

print("\n" + "=" * 60)
print("To test with auth token:")
print("1. Open browser DevTools (F12)")
print("2. Go to Application tab → Local Storage")
print("3. Find your auth token")
print("4. Call export endpoint with: Authorization: Bearer {token}")
print("=" * 60)
