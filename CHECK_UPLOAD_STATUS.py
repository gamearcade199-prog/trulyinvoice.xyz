import httpx
import asyncio

async def check_upload_status():
    """Check documents and invoices tables to see where uploaded files are"""
    
    print("=" * 100)
    print("🔍 CHECKING UPLOAD STATUS - DOCUMENTS & INVOICES")
    print("=" * 100)
    
    SUPABASE_URL = "https://ldvwxqluaheuhbycdpwn.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A"
    
    async with httpx.AsyncClient() as client:
        # Check documents table
        print("\n📄 CHECKING DOCUMENTS TABLE:")
        print("-" * 100)
        docs_response = await client.get(
            f"{SUPABASE_URL}/rest/v1/documents",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}"
            },
            params={"select": "*", "order": "created_at.desc", "limit": "10"}
        )
        
        if docs_response.status_code == 200:
            documents = docs_response.json()
            print(f"Found {len(documents)} recent document(s)")
            
            if documents:
                for i, doc in enumerate(documents, 1):
                    user_id = doc.get('user_id', 'NULL')
                    print(f"\n  Document #{i}:")
                    print(f"    ID: {doc.get('id')}")
                    print(f"    File Name: {doc.get('file_name', 'N/A')}")
                    print(f"    Status: {doc.get('status', 'N/A')}")
                    print(f"    User ID: {user_id[:20] if user_id and user_id != 'NULL' else 'NULL'}...")
                    print(f"    Created: {doc.get('created_at', 'N/A')}")
                    print(f"    Storage Path: {doc.get('storage_path', 'N/A')}")
            else:
                print("  ❌ No documents found!")
        else:
            print(f"  ❌ Error: {docs_response.status_code}")
        
        # Check invoices table
        print("\n\n💰 CHECKING INVOICES TABLE:")
        print("-" * 100)
        inv_response = await client.get(
            f"{SUPABASE_URL}/rest/v1/invoices",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}"
            },
            params={"select": "*", "order": "created_at.desc", "limit": "10"}
        )
        
        if inv_response.status_code == 200:
            invoices = inv_response.json()
            print(f"Found {len(invoices)} invoice(s)")
            
            if invoices:
                for i, inv in enumerate(invoices, 1):
                    user_id = inv.get('user_id', 'NULL')
                    print(f"\n  Invoice #{i}:")
                    print(f"    ID: {inv.get('id')}")
                    print(f"    Vendor: {inv.get('vendor_name', 'N/A')}")
                    print(f"    Amount: ₹{inv.get('total_amount', 0)}")
                    print(f"    Invoice #: {inv.get('invoice_number', 'N/A')}")
                    print(f"    User ID: {user_id[:20] if user_id and user_id != 'NULL' else 'NULL'}...")
                    print(f"    Document ID: {inv.get('document_id', 'N/A')}")
                    print(f"    Created: {inv.get('created_at', 'N/A')}")
            else:
                print("  ❌ No invoices found!")
        else:
            print(f"  ❌ Error: {inv_response.status_code}")
        
        print("\n" + "=" * 100)
        print("📋 ANALYSIS:")
        print("=" * 100)
        
        if docs_response.status_code == 200 and inv_response.status_code == 200:
            documents = docs_response.json()
            invoices = inv_response.json()
            
            if len(documents) > 0 and len(invoices) == 0:
                print("\n⚠️  ISSUE: Documents uploaded but NOT processed into invoices!")
                print("\nPossible causes:")
                print("  1. Backend processing failed")
                print("  2. Backend not running")
                print("  3. AI extraction error")
                print("\n💡 SOLUTION:")
                print("  1. Make sure backend is running: cd backend && python -m uvicorn app.main:app --reload")
                print("  2. Check backend logs for errors")
                print("  3. Try re-processing: POST http://localhost:8000/api/documents/{id}/process")
            
            elif len(documents) == 0 and len(invoices) == 0:
                print("\n⚠️  ISSUE: No documents or invoices found!")
                print("\nPossible causes:")
                print("  1. Upload failed silently")
                print("  2. User not logged in")
                print("  3. Supabase storage/database issue")
                print("\n💡 SOLUTION:")
                print("  1. Check browser console for upload errors")
                print("  2. Verify you're logged in")
                print("  3. Check Supabase connection")
            
            elif len(invoices) > 0:
                print("\n✅ Invoices exist in database!")
                print("\nBut frontend shows 'No invoices found'?")
                print("\nPossible causes:")
                print("  1. User ID mismatch (logged in as different user)")
                print("  2. Frontend not refreshing")
                print("  3. Browser cache issue")
                print("\n💡 SOLUTION:")
                print("  1. Hard refresh: Ctrl+Shift+R")
                print("  2. Check which user you're logged in as")
                print("  3. Clear browser cache")
        
        print("=" * 100)

if __name__ == "__main__":
    asyncio.run(check_upload_status())
