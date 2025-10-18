#!/usr/bin/env python3
"""
Simulate EXACTLY what the Next.js frontend does when fetching invoice details
"""
import requests

VERCEL_FRONTEND = "https://trulyinvoice.xyz"
RENDER_BACKEND = "https://trulyinvoice-backend.onrender.com"
TEST_ID = "03bf3a77-0c3d-4adc-9949-0f085a1f13be"

print("=" * 80)
print("🔍 SIMULATING NEXT.JS FRONTEND BEHAVIOR")
print("=" * 80)

# What the Next.js page does:
# 1. It's at: https://trulyinvoice.xyz/invoices/03bf3a77-0c3d-4adc-9949-0f085a1f13be
# 2. It reads process.env.NEXT_PUBLIC_API_URL
# 3. It does: fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/invoices/${invoiceId}`)

print(f"\n📍 Frontend page: {VERCEL_FRONTEND}/invoices/{TEST_ID}")
print(f"🔗 API_URL env: {RENDER_BACKEND}")
print(f"📡 Fetch URL: {RENDER_BACKEND}/api/invoices/{TEST_ID}")

# Test what happens when Next.js fetches from browser
print("\n1️⃣ Browser fetch simulation (from trulyinvoice.xyz)...")
try:
    # Browser would NOT include Referer to a different domain (security)
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Origin": "https://trulyinvoice.xyz"
    }
    response = requests.get(
        f"{RENDER_BACKEND}/api/invoices/{TEST_ID}",
        headers=headers,
        timeout=10,
        allow_redirects=True
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Got invoice: {data.get('vendor_name')}")
        print(f"   Total Amount: {data.get('total_amount')}")
    else:
        print(f"   ❌ Error: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test with RSC (React Server Components) headers
print("\n2️⃣ With Next.js RSC headers...")
try:
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Origin": "https://trulyinvoice.xyz",
        "rsc": "1"  # Next.js RSC marker
    }
    response = requests.get(
        f"{RENDER_BACKEND}/api/invoices/{TEST_ID}",
        headers=headers,
        timeout=10
    )
    print(f"   Status: {response.status_code}")
    if response.status_code != 200:
        print(f"   ❌ Error: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test connection timeout scenarios
print("\n3️⃣ Testing connection resilience...")
try:
    response = requests.get(
        f"{RENDER_BACKEND}/api/invoices/{TEST_ID}",
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response time: OK")
except requests.Timeout:
    print(f"   ❌ TIMEOUT - Backend took too long to respond")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test if the issue is with the page rendering
print("\n4️⃣ Testing page load (simulating browser navigation)...")
try:
    # First, load the page itself
    page_response = requests.get(
        f"{VERCEL_FRONTEND}/invoices/{TEST_ID}",
        timeout=10,
        allow_redirects=True
    )
    print(f"   Page status: {page_response.status_code}")
    
    # Then try the API call
    if page_response.status_code == 200:
        api_response = requests.get(
            f"{RENDER_BACKEND}/api/invoices/{TEST_ID}",
            headers={"Origin": "https://trulyinvoice.xyz"},
            timeout=10
        )
        print(f"   API status: {api_response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 80)
print("✅ Check results above")
print("=" * 80)
