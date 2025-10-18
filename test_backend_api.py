#!/usr/bin/env python3
"""
Test the deployed backend API to see what's happening with the 404 errors
"""
import requests
import json
from urllib.parse import quote

# Test invoice IDs from your database
TEST_IDS = [
    "03bf3a77-0c3d-4adc-9949-0f085a1f13be",
    "8507ec01-5117-4148-8858-eeb2584e2863",
    "357a0e56-f383-4564-8e03-8808948a25d1"
]

BACKEND_URL = "https://trulyinvoice-backend.onrender.com"

print("=" * 80)
print("🧪 TESTING BACKEND API")
print("=" * 80)

# Test 1: Check if backend is up
print("\n1️⃣ Testing Backend Health...")
try:
    response = requests.get(f"{BACKEND_URL}/health", timeout=10)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:100]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Get all invoices
print("\n2️⃣ Testing GET /api/invoices (list all)...")
try:
    response = requests.get(f"{BACKEND_URL}/api/invoices", timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Found {len(data)} invoices")
        if data:
            print(f"   Sample IDs: {[inv.get('id') for inv in data[:2]]}")
    else:
        print(f"   Response: {response.text[:100]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Get specific invoice (with raw UUID)
print("\n3️⃣ Testing GET /api/invoices/{id} with raw UUID...")
for test_id in TEST_IDS[:1]:
    try:
        url = f"{BACKEND_URL}/api/invoices/{test_id}"
        print(f"   URL: {url}")
        response = requests.get(url, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found: {data.get('vendor_name', 'Unknown')}")
        else:
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

# Test 4: Get specific invoice (with encoded UUID)
print("\n4️⃣ Testing GET /api/invoices/{id} with encoded UUID...")
for test_id in TEST_IDS[:1]:
    try:
        encoded_id = quote(test_id, safe='-')
        url = f"{BACKEND_URL}/api/invoices/{encoded_id}"
        print(f"   URL: {url}")
        response = requests.get(url, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found: {data.get('vendor_name', 'Unknown')}")
        else:
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

# Test 5: Check headers
print("\n5️⃣ Checking API Headers...")
try:
    response = requests.head(f"{BACKEND_URL}/api/invoices", timeout=10)
    print(f"   Status: {response.status_code}")
    print(f"   Headers:")
    for key in ['content-type', 'access-control-allow-origin', 'server']:
        print(f"      {key}: {response.headers.get(key, 'NOT SET')}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 80)
print("✅ TEST COMPLETE - Check output above for issues")
print("=" * 80)
