"""
Quick script to check for dummy/test invoices in database
"""
from supabase import create_client

SUPABASE_URL = 'https://ldvwxqluaheuhbycdpwn.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A'

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("=" * 60)
print("🔍 CHECKING FOR DUMMY/TEST INVOICES IN DATABASE")
print("=" * 60)

# Fetch all invoices
response = supabase.table('invoices').select('*').execute()

print(f"\n📊 Total invoices in database: {len(response.data)}\n")

# Check for invoices with NULL user_id
null_user_invoices = [inv for inv in response.data if inv.get('user_id') is None]
print(f"⚠️  Invoices with NULL user_id: {len(null_user_invoices)}")

if null_user_invoices:
    print("\n🚨 FOUND DUMMY INVOICES (NULL user_id):")
    for i, inv in enumerate(null_user_invoices, 1):
        print(f"  {i}. ID: {inv['id']}")
        print(f"     Vendor: {inv.get('vendor_name', 'N/A')}")
        print(f"     Amount: ₹{inv.get('total_amount', 0)}")
        print(f"     Invoice #: {inv.get('invoice_number', 'N/A')}")
        print(f"     Created: {inv.get('created_at', 'N/A')}")
        print()

# Check for real user invoices
real_invoices = [inv for inv in response.data if inv.get('user_id') is not None]
print(f"✅ Real user invoices: {len(real_invoices)}")

if real_invoices:
    print("\n📋 REAL USER INVOICES:")
    for i, inv in enumerate(real_invoices, 1):
        user_id = inv.get('user_id', '')
        print(f"  {i}. Vendor: {inv.get('vendor_name', 'N/A')}")
        print(f"     Amount: ₹{inv.get('total_amount', 0)}")
        print(f"     User: {user_id[:12]}..." if user_id else "     User: N/A")
        print()

print("=" * 60)
print("🔍 DIAGNOSIS:")
print("=" * 60)

if null_user_invoices:
    print("❌ ISSUE FOUND: You have dummy invoices with NULL user_id")
    print("   These are being displayed because of this query:")
    print("   .or(`user_id.eq.${user.id},user_id.is.null`)")
    print("\n💡 SOLUTION:")
    print("   1. Remove the '.or(user_id.is.null)' condition")
    print("   2. Delete dummy invoices from database")
else:
    print("✅ No dummy invoices found!")
    print("   If you're still seeing dummy data, check the frontend code")
    print("   for hardcoded sample data.")

print("=" * 60)
