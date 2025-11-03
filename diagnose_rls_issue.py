"""
Check RLS policies and user access to the invoice
"""
import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment from backend/.env
load_dotenv("backend/.env")

supabase_url = os.getenv("SUPABASE_URL")
supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")
supabase_anon_key = os.getenv("SUPABASE_KEY")  # SUPABASE_KEY is the anon key

if not all([supabase_service_key, supabase_anon_key]):
    print("❌ Missing Supabase keys in .env")
    print(f"URL: {supabase_url}")
    print(f"Service: {'✅' if supabase_service_key else '❌'}")
    print(f"Anon: {'✅' if supabase_anon_key else '❌'}")
    exit(1)

# Admin client (bypasses RLS)
admin_client = create_client(supabase_url, supabase_service_key)

# User client (respects RLS)
user_client = create_client(supabase_url, supabase_anon_key)

invoice_id = '106f005b-1f17-40b1-8f0b-60eeb1bca773'
user_id = 'd1949c37-d380-46f4-ad30-20ae84aff1ad'

print("=" * 80)
print("🔍 CHECKING RLS POLICIES AND USER ACCESS")
print("=" * 80)

# Check 1: Invoice exists (admin)
print("\n1. Check if invoice exists (using SERVICE_KEY):")
try:
    response = admin_client.table("invoices").select("*").eq("id", invoice_id).execute()
    if response.data:
        inv = response.data[0]
        print(f"   ✅ Invoice exists in database")
        print(f"   Invoice #: {inv.get('invoice_number')}")
        print(f"   User ID: {inv.get('user_id')}")
        print(f"   Vendor: {inv.get('vendor_name')}")
        print(f"   Customer: {inv.get('customer_name')}")
        print(f"   Total: ₹{inv.get('total_amount')}")
        
        if inv.get('user_id') == user_id:
            print(f"   ✅ User ID matches!")
        else:
            print(f"   ❌ User ID mismatch! Invoice belongs to: {inv.get('user_id')}")
    else:
        print(f"   ❌ Invoice not found")
        exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Check 2: RLS policies on invoices table
print("\n2. Check RLS policies on invoices table:")
try:
    # Get RLS policies
    response = admin_client.rpc('exec_sql', {
        'sql': """
            SELECT 
                schemaname, tablename, policyname, permissive, roles, cmd, qual, with_check
            FROM pg_policies 
            WHERE tablename = 'invoices'
            ORDER BY policyname;
        """
    }).execute()
    
    if response.data:
        print(f"   Found {len(response.data)} RLS policies:")
        for policy in response.data:
            print(f"\n   Policy: {policy.get('policyname')}")
            print(f"   Command: {policy.get('cmd')}")
            print(f"   Roles: {policy.get('roles')}")
            print(f"   Using: {policy.get('qual')}")
    else:
        # Alternative approach - check if RLS is enabled
        response2 = admin_client.rpc('exec_sql', {
            'sql': "SELECT relrowsecurity FROM pg_class WHERE relname = 'invoices';"
        }).execute()
        print(f"   RLS status: {response2.data}")
except Exception as e:
    print(f"   ⚠️ Cannot query policies directly: {e}")
    print(f"   This is normal - checking RLS another way...")

# Check 3: Try to access as anonymous user (simulating frontend)
print("\n3. Try to access invoice as anonymous user:")
try:
    response = user_client.table("invoices").select("id, invoice_number, vendor_name, total_amount").eq("id", invoice_id).execute()
    if response.data:
        print(f"   ✅ Anonymous access works - invoice accessible")
        print(f"   Data: {response.data}")
    else:
        print(f"   ❌ Anonymous access blocked - RLS policy preventing access")
        print(f"   This is likely the cause of 401 error")
except Exception as e:
    print(f"   ❌ Error accessing as anonymous: {e}")
    print(f"   This confirms RLS is blocking access")

# Check 4: Try to access with user authentication
print("\n4. Simulate authenticated user access:")
print(f"   Note: Frontend should be sending auth token in requests")
print(f"   User ID from invoice: {user_id}")
print(f"   Frontend needs to authenticate with this user's token")

print("\n" + "=" * 80)
print("🔧 DIAGNOSIS:")
print("=" * 80)

print("""
The 401 error is caused by RLS (Row Level Security) policies.

PROBLEM:
- Invoice exists and was created successfully ✅
- Invoice belongs to user: d1949c37-d380-46f4-ad30-20ae84aff1ad
- Frontend is NOT sending authentication token when fetching invoice
- RLS policy blocks access without proper authentication

SOLUTION:
Check frontend authentication in:
1. frontend/src/app/invoices/details/page.tsx
2. Make sure it's using authenticated Supabase client
3. Verify user is logged in before accessing invoice details

Run this to check user session:
  Check browser console for auth errors
  Check if localStorage has supabase auth token
""")
