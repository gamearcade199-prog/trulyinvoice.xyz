#!/usr/bin/env python3
"""
Test if the 404 issue is fixed on deployed Vercel site
"""
import requests
import time

print("=" * 80)
print("🧪 TESTING IF 404 ISSUE IS FIXED")
print("=" * 80)

VERCEL_URL = "https://trulyinvoice.xyz"
TEST_INVOICE_ID = "03bf3a77-0c3d-4adc-9949-0f085a1f13be"

print("\n⏳ Waiting a moment for Vercel deployment to complete...")
time.sleep(5)

# Test 1: Test API endpoint
print("\n1️⃣ Testing API route (should work)...")
try:
    response = requests.get(
        f"{VERCEL_URL}/api/test-invoice/12345",
        timeout=10,
        allow_redirects=True
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Response: {response.json()}")
    else:
        print(f"   ❌ Error: {response.text[:100]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Test invoice detail page
print("\n2️⃣ Testing /invoices/[id] page...")
try:
    response = requests.get(
        f"{VERCEL_URL}/invoices/{TEST_INVOICE_ID}",
        timeout=10,
        allow_redirects=True
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ PAGE LOADS SUCCESSFULLY!")
        # Check if it contains the page markup
        if "invoice" in response.text.lower() or "details" in response.text.lower():
            print(f"   ✅ Page content looks correct")
    else:
        print(f"   ❌ Still getting 404")
        print(f"   Response preview: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Test with browser headers
print("\n3️⃣ Testing with browser-like headers...")
try:
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml"
    }
    response = requests.get(
        f"{VERCEL_URL}/invoices/{TEST_INVOICE_ID}",
        headers=headers,
        timeout=10,
        allow_redirects=True
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Works with browser headers too")
    else:
        print(f"   ❌ Still 404 with browser headers")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 80)
print("✅ TEST COMPLETE")
print("=" * 80)
