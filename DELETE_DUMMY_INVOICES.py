"""
DELETE DUMMY INVOICES WITH NULL user_id
Run this to clean up your database
"""
import httpx
import asyncio

async def delete_dummy_invoices():
    print("=" * 80)
    print("🗑️  CLEANING UP DUMMY INVOICES FROM DATABASE")
    print("=" * 80)
    
    SUPABASE_URL = "https://ldvwxqluaheuhbycdpwn.supabase.co"
    # Using service key for delete operations (you may need to use anon key depending on RLS)
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A"
    
    async with httpx.AsyncClient() as client:
        # First, get all invoices with NULL user_id
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/invoices",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}"
            },
            params={"select": "*", "user_id": "is.null"}
        )
        
        if response.status_code == 200:
            dummy_invoices = response.json()
            
            if not dummy_invoices:
                print("\n✅ No dummy invoices found! Database is clean.")
                print("=" * 80)
                return
            
            print(f"\nFound {len(dummy_invoices)} dummy invoice(s) to delete:")
            for inv in dummy_invoices:
                print(f"  - {inv.get('vendor_name', 'N/A')} (ID: {inv.get('id')})")
            
            confirm = input(f"\n⚠️  Delete these {len(dummy_invoices)} invoice(s)? (yes/no): ")
            
            if confirm.lower() != 'yes':
                print("\n❌ Deletion cancelled.")
                return
            
            # Delete invoices with NULL user_id
            delete_response = await client.delete(
                f"{SUPABASE_URL}/rest/v1/invoices",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Prefer": "return=minimal"
                },
                params={"user_id": "is.null"}
            )
            
            if delete_response.status_code in [200, 204]:
                print(f"\n✅ Successfully deleted {len(dummy_invoices)} dummy invoice(s)!")
                print("\n🎉 Your database is now clean!")
                print("   Refresh your frontend to see only real invoices.")
            else:
                print(f"\n❌ Failed to delete invoices: {delete_response.status_code}")
                print(f"   Error: {delete_response.text}")
                print("\n💡 You may need to delete them manually in Supabase dashboard:")
                print("   1. Go to https://supabase.com/dashboard")
                print("   2. Select your project")
                print("   3. Go to Table Editor → invoices")
                print("   4. Filter for NULL user_id and delete")
        else:
            print(f"❌ Error fetching invoices: {response.status_code}")
    
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(delete_dummy_invoices())
