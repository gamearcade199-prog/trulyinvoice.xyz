import httpx
import asyncio

async def full_diagnostic():
    """Complete diagnostic to find dummy invoice issues"""
    
    print("=" * 100)
    print("🔍 TRULYINVOICE DEEP SCAN - FINDING DUMMY INVOICE ISSUES")
    print("=" * 100)
    
    async with httpx.AsyncClient() as client:
        # Check invoices
        response = await client.get(
            "https://ldvwxqluaheuhbycdpwn.supabase.co/rest/v1/invoices",
            headers={
                "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A"
            },
            params={"select": "*"}
        )
        
        if response.status_code == 200:
            invoices = response.json()
            print(f"\n📊 Total Invoices in Database: {len(invoices)}")
            print("-" * 100)
            
            null_user = [inv for inv in invoices if inv.get('user_id') is None]
            real_user = [inv for inv in invoices if inv.get('user_id') is not None]
            
            if null_user:
                print(f"\n🚨 ISSUE FOUND: {len(null_user)} invoices with NULL user_id (DUMMY DATA)")
                print("-" * 100)
                for i, inv in enumerate(null_user, 1):
                    print(f"\n  Invoice #{i}:")
                    print(f"    ID: {inv.get('id')}")
                    print(f"    Vendor: {inv.get('vendor_name', 'N/A')}")
                    print(f"    Amount: ₹{inv.get('total_amount', 0)}")
                    print(f"    Invoice Number: {inv.get('invoice_number', 'N/A')}")
                    print(f"    User ID: NULL ⚠️  <-- THIS IS THE PROBLEM")
                    print(f"    Created: {inv.get('created_at', 'N/A')}")
            else:
                print("\n✅ No NULL user_id invoices found in database")
            
            if real_user:
                print(f"\n\n✅ Real User Invoices: {len(real_user)}")
                print("-" * 100)
                for i, inv in enumerate(real_user, 1):
                    user_id = inv.get('user_id', '')
                    print(f"\n  Invoice #{i}:")
                    print(f"    Vendor: {inv.get('vendor_name', 'N/A')}")
                    print(f"    Amount: ₹{inv.get('total_amount', 0)}")
                    print(f"    Invoice Number: {inv.get('invoice_number', 'N/A')}")
                    print(f"    User ID: {user_id[:20]}... ✅")
            
            print("\n" + "=" * 100)
            print("📋 DIAGNOSIS & SOLUTION")
            print("=" * 100)
            
            if null_user:
                print("\n❌ ROOT CAUSE IDENTIFIED:")
                print("   The frontend query is fetching invoices with NULL user_id")
                print("\n📍 Problematic Code Locations:")
                print("   1. frontend/src/app/invoices/page.tsx (Line ~60)")
                print("      .or(`user_id.eq.${user.id},user_id.is.null`)")
                print("\n   2. frontend/src/app/dashboard/page.tsx (Similar query)")
                print("\n💡 REQUIRED FIXES:")
                print("   ✓ Remove '.or(user_id.is.null)' from invoices query")
                print("   ✓ Remove '.or(user_id.is.null)' from dashboard query")
                print("   ✓ Delete NULL user_id invoices from database")
                print("\n🔧 Commands to fix:")
                print("   I will now create the fix files for you...")
            else:
                print("\n✅ Database is clean!")
                print("   If you still see dummy data, it's likely:")
                print("   - Mock data in the landing page (page.tsx) - this is intentional for demo")
                print("   - Cached data in browser - try hard refresh (Ctrl+Shift+R)")
            
            print("=" * 100)
            
        else:
            print(f"❌ Error fetching invoices: {response.status_code}")
            print(f"   {response.text}")

if __name__ == "__main__":
    asyncio.run(full_diagnostic())
