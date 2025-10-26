"""
Quick Fix: Process one document manually to test
"""
import httpx
import asyncio
import os
from pathlib import Path

# Your Supabase credentials
SUPABASE_URL = "https://ldvwxqluaheuhbycdpwn.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDA3NjY1NiwiZXhwIjoyMDc1NjUyNjU2fQ.939ySYuwA9ByCprCiI9GL5xEmvkhONYEWdtuHVLweWM"

async def test_storage_access():
    """Test if we can access storage"""
    
    print("=" * 80)
    print("🧪 TESTING STORAGE ACCESS")
    print("=" * 80)
    
    # Get the most recent document
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Fetch a document
        print("\n1️⃣  Fetching recent document...")
        docs_response = await client.get(
            f"{SUPABASE_URL}/rest/v1/documents",
            headers={
                "apikey": SUPABASE_SERVICE_KEY,
                "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}"
            },
            params={"select": "*", "status": "eq.uploaded", "limit": "1", "order": "created_at.desc"}
        )
        
        if docs_response.status_code != 200:
            print(f"❌ Failed to fetch document: {docs_response.status_code}")
            return
        
        documents = docs_response.json()
        if not documents:
            print("❌ No uploaded documents found!")
            return
        
        doc = documents[0]
        storage_path = doc.get('storage_path')
        doc_id = doc['id']
        file_name = doc.get('file_name', 'unknown.pdf')
        
        print(f"✅ Found document: {file_name}")
        print(f"   ID: {doc_id}")
        print(f"   Storage path: {storage_path}")
        
        # Try to download from storage
        print("\n2️⃣  Attempting to download from storage...")
        
        # Method 1: Direct storage API with service key
        storage_url = f"{SUPABASE_URL}/storage/v1/object/invoice-documents/{storage_path}"
        print(f"   URL: {storage_url[:80]}...")
        
        try:
            download_response = await client.get(
                storage_url,
                headers={
                    "apikey": SUPABASE_SERVICE_KEY,
                    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}"
                },
                timeout=30.0
            )
            
            print(f"   Status: {download_response.status_code}")
            
            if download_response.status_code == 200:
                print(f"   ✅ SUCCESS! Downloaded {len(download_response.content)} bytes")
                
                # Save to temp file
                temp_dir = Path("temp_downloads")
                temp_dir.mkdir(exist_ok=True)
                temp_file = temp_dir / file_name
                
                with open(temp_file, 'wb') as f:
                    f.write(download_response.content)
                
                print(f"   💾 Saved to: {temp_file}")
                
                # Now try to process via backend
                print("\n3️⃣  Triggering backend processing...")
                process_response = await client.post(
                    f"http://localhost:8000/api/documents/{doc_id}/process",
                    headers={"Content-Type": "application/json"},
                    timeout=60.0
                )
                
                print(f"   Backend status: {process_response.status_code}")
                
                if process_response.status_code == 200:
                    result = process_response.json()
                    print(f"   ✅ PROCESSING SUCCESSFUL!")
                    print(f"   Vendor: {result.get('vendor_name', 'N/A')}")
                    print(f"   Amount: ₹{result.get('total_amount', 0)}")
                else:
                    error = process_response.text
                    print(f"   ❌ Processing failed:")
                    print(f"   {error[:200]}")
                
            else:
                print(f"   ❌ Download failed: {download_response.status_code}")
                print(f"   Response: {download_response.text[:200]}")
                
                # Check bucket permissions
                print("\n🔍 ISSUE: Storage bucket not accessible")
                print("\n💡 SOLUTION: Make bucket public in Supabase")
                print("   1. Go to https://supabase.com/dashboard/project/ldvwxqluaheuhbycdpwn/storage/buckets")
                print("   2. Find 'invoice-documents' bucket")
                print("   3. Click settings → Make bucket PUBLIC")
                print("   4. Add RLS policy to allow authenticated reads")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_storage_access())
