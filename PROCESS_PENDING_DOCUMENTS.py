"""
Process all pending documents that have been uploaded but not processed
"""
import httpx
import asyncio

async def process_pending_documents():
    print("=" * 100)
    print("🔄 PROCESSING PENDING DOCUMENTS")
    print("=" * 100)
    
    SUPABASE_URL = "https://ldvwxqluaheuhbycdpwn.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A"
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Get all uploaded documents
        docs_response = await client.get(
            f"{SUPABASE_URL}/rest/v1/documents",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}"
            },
            params={"select": "*", "status": "eq.uploaded", "order": "created_at.desc"}
        )
        
        if docs_response.status_code != 200:
            print(f"❌ Failed to fetch documents: {docs_response.status_code}")
            return
        
        documents = docs_response.json()
        print(f"\nFound {len(documents)} pending document(s) to process\n")
        
        if not documents:
            print("✅ No pending documents!")
            return
        
        # Check if backend is running
        try:
            health_check = await client.get("http://localhost:8000/health", timeout=5.0)
            if health_check.status_code != 200:
                print("❌ Backend is not responding!")
                print("   Please start backend: cd backend && python -m uvicorn app.main:app --reload")
                return
            print("✅ Backend is running\n")
        except Exception as e:
            print(f"❌ Backend is not running: {e}")
            print("   Please start backend: cd backend && python -m uvicorn app.main:app --reload")
            return
        
        # Process each document
        for i, doc in enumerate(documents[:5], 1):  # Process max 5 at a time
            doc_id = doc['id']
            file_name = doc.get('file_name', 'Unknown')
            
            print(f"[{i}/{min(len(documents), 5)}] Processing: {file_name}")
            print(f"     Document ID: {doc_id}")
            
            try:
                # Call backend processing endpoint
                process_response = await client.post(
                    f"http://localhost:8000/api/documents/{doc_id}/process",
                    headers={"Content-Type": "application/json"},
                    timeout=60.0
                )
                
                if process_response.status_code == 200:
                    result = process_response.json()
                    print(f"     ✅ SUCCESS - Extracted: {result.get('vendor_name', 'N/A')}")
                    print(f"        Amount: ₹{result.get('total_amount', 0)}")
                else:
                    error_text = process_response.text
                    print(f"     ❌ FAILED - Status {process_response.status_code}")
                    print(f"        Error: {error_text[:100]}")
                
            except Exception as e:
                print(f"     ❌ ERROR: {str(e)[:100]}")
            
            print()
        
        if len(documents) > 5:
            print(f"\nℹ️  {len(documents) - 5} more documents pending. Run script again to process more.")
        
        print("=" * 100)
        print("🎉 PROCESSING COMPLETE!")
        print("\nNext steps:")
        print("  1. Hard refresh your browser (Ctrl+Shift+R)")
        print("  2. Go to http://localhost:3000/invoices")
        print("  3. You should now see your processed invoices!")
        print("=" * 100)

if __name__ == "__main__":
    asyncio.run(process_pending_documents())
