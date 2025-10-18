#!/usr/bin/env python3
"""
Test backend API with different scenarios to debug why it works locally but not on live
"""
import requests
import json

BACKEND_URL = "https://trulyinvoice-backend.onrender.com"
TEST_ID = "03bf3a77-0c3d-4adc-9949-0f085a1f13be"

print("=" * 80)
print("🧪 DEBUGGING: Why does it work locally but fail on live?")
print("=" * 80)

# Test 1: Direct call (what local would do)
print("\n1️⃣ Direct call (simulating local)...")
try:
    response = requests.get(
        f"{BACKEND_URL}/api/invoices/{TEST_ID}",
        timeout=10,
        headers={"User-Agent": "Python-Requests"}
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json() if response.status_code == 200 else response.text[:100]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: With browser-like headers (what Vercel would do)
print("\n2️⃣ Browser-like headers (simulating Vercel/browser)...")
try:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Origin": "https://trulyinvoice.xyz",
        "Referer": "https://trulyinvoice.xyz/invoices/03bf3a77-0c3d-4adc-9949-0f085a1f13be"
    }
    response = requests.get(
        f"{BACKEND_URL}/api/invoices/{TEST_ID}",
        timeout=10,
        headers=headers
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json() if response.status_code == 200 else response.text[:100]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: With CORS preflight check
print("\n3️⃣ CORS preflight (OPTIONS request)...")
try:
    headers = {
        "Origin": "https://trulyinvoice.xyz",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "content-type"
    }
    response = requests.options(
        f"{BACKEND_URL}/api/invoices/{TEST_ID}",
        timeout=10,
        headers=headers
    )
    print(f"   Status: {response.status_code}")
    print(f"   CORS Headers:")
    for key in ["Access-Control-Allow-Origin", "Access-Control-Allow-Methods", "Access-Control-Allow-Headers"]:
        value = response.headers.get(key, "NOT SET")
        print(f"      {key}: {value}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Check if it's a redirect issue
print("\n4️⃣ Checking for redirects...")
try:
    response = requests.get(
        f"{BACKEND_URL}/api/invoices/{TEST_ID}",
        timeout=10,
        allow_redirects=False
    )
    print(f"   Status: {response.status_code}")
    print(f"   Redirect: {response.headers.get('Location', 'No redirect')}")
    if response.status_code >= 300 and response.status_code < 400:
        print(f"   ⚠️ Got redirect to: {response.headers.get('Location')}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: Test with different content types
print("\n5️⃣ Different Accept headers...")
for accept_type in ["application/json", "text/html", "*/*"]:
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/invoices/{TEST_ID}",
            timeout=10,
            headers={"Accept": accept_type}
        )
        print(f"   Accept: {accept_type:20} → Status: {response.status_code}")
    except Exception as e:
        print(f"   Accept: {accept_type:20} → Error: {e}")

# Test 6: Check response headers for live vs local differences
print("\n6️⃣ Full response headers analysis...")
try:
    response = requests.get(
        f"{BACKEND_URL}/api/invoices/{TEST_ID}",
        timeout=10
    )
    print(f"   Status: {response.status_code}")
    print(f"   Important headers:")
    for key in ["content-type", "content-length", "server", "cache-control", "access-control-allow-origin"]:
        value = response.headers.get(key, "NOT SET")
        print(f"      {key}: {value}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 80)
print("✅ Analysis complete")
print("=" * 80)
