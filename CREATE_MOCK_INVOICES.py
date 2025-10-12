"""
SIMPLE MOCK PROCESSOR - Bypass AI and create invoices from your uploaded documents
This will process your uploads WITHOUT AI, using basic filename parsing
"""
import httpx
import asyncio
from datetime import datetime

SUPABASE_URL = "https://ldvwxqluaheuhbycdpwn.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDA3NjY1NiwiZXhwIjoyMDc1NjUyNjU2fQ.939ySYuwA9ByCprCiI9GL5xEmvkhONYEWdtuHVLweWM"

async def create_invoices_from_documents():
    """Create invoice records from uploaded documents"""
    
    print("=" * 100)
    print("🚀 MOCK PROCESSOR - Creating Invoices Without AI")
    print("=" * 100)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        headers = {
            "apikey": SUPABASE_SERVICE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        
        # Get uploaded documents
        docs_response = await client.get(
            f"{SUPABASE_URL}/rest/v1/documents",
            headers=headers,
            params={"select": "*", "status": "eq.uploaded", "order": "created_at.desc"}
        )
        
        if docs_response.status_code != 200:
            print(f"❌ Failed to fetch documents: {docs_response.status_code}")
            return
        
        documents = docs_response.json()
        print(f"\n📄 Found {len(documents)} documents to process\n")
        
        if not documents:
            print("✅ No pending documents!")
            return
        
        # Process each document
        for i, doc in enumerate(documents, 1):
            doc_id = doc['id']
            user_id = doc['user_id']
            file_name = doc.get('file_name', 'Invoice')
            
            print(f"[{i}/{len(documents)}] Processing: {file_name}")
            
            # Extract invoice number from filename (if it exists)
            import re
            invoice_num_match = re.search(r'#?([\d-]+)', file_name)
            invoice_number = invoice_num_match.group(1) if invoice_num_match else f"INV-{datetime.now().strftime('%Y%m%d')}-{i:03d}"
            
            # Extract date from filename or use creation date
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', file_name)
            invoice_date = date_match.group(1) if date_match else doc['created_at'].split('T')[0]
            
            # Create mock invoice data
            invoice_data = {
                "user_id": user_id,
                "document_id": doc_id,
                "vendor_name": "Extracted from Document",  # Basic vendor name
                "invoice_number": invoice_number,
                "invoice_date": invoice_date,
                "subtotal": 10000.0,  # Mock amount
                "cgst": 900.0,
                "sgst": 900.0,
                "igst": 0.0,
                "total_amount": 11800.0,
                "payment_status": "unpaid",
                "created_at": datetime.utcnow().isoformat()
            }
            
            try:
                # Insert invoice
                invoice_response = await client.post(
                    f"{SUPABASE_URL}/rest/v1/invoices",
                    headers=headers,
                    json=invoice_data
                )
                
                if invoice_response.status_code in [200, 201]:
                    result = invoice_response.json()
                    print(f"     ✅ Invoice created: #{invoice_number} - ₹11,800")
                    
                    # Update document status
                    await client.patch(
                        f"{SUPABASE_URL}/rest/v1/documents?id=eq.{doc_id}",
                        headers=headers,
                        json={"status": "processed"}
                    )
                else:
                    print(f"     ❌ Failed: {invoice_response.status_code}")
                    print(f"        {invoice_response.text[:100]}")
            
            except Exception as e:
                print(f"     ❌ Error: {e}")
        
        print("\n" + "=" * 100)
        print("🎉 PROCESSING COMPLETE!")
        print("\n✅ All documents have been converted to invoices (with mock data)")
        print("\nℹ️  Note: These are MOCK invoices with sample amounts")
        print("   To get REAL data extraction, you need to:")
        print("   1. Fix OpenAI/httpx version issues")
        print("   2. Or use a different AI service")
        print("\nNext steps:")
        print("  1. Go to http://localhost:3000/invoices")
        print("  2. Press Ctrl+Shift+R to refresh")
        print("  3. You should see all your invoices!")
        print("=" * 100)

if __name__ == "__main__":
    asyncio.run(create_invoices_from_documents())
