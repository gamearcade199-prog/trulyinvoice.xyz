"""
PRODUCTION STORAGE SETUP AND FILE RECOVERY
Fix storage issues and locate user's uploaded PDF
"""

import asyncio
import httpx
import json
from datetime import datetime

# Supabase config
SUPABASE_URL = "https://ldvwxqluaheuhbycdpwn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNzY2NTYsImV4cCI6MjA3NTY1MjY1Nn0.uPBCzeJ3tH1SD0QObL850zcrKDDLr9TA6KCUzBp9e1A"

class StorageManager:
    """Production-grade storage management"""
    
    def __init__(self):
        self.client = None
        self.bucket_name = "invoice-documents"
    
    async def __aenter__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
    
    async def create_bucket_if_not_exists(self):
        """Create storage bucket with proper policies"""
        print("1. Creating storage bucket...")
        
        # Create bucket
        try:
            response = await self.client.post(
                f"{SUPABASE_URL}/storage/v1/bucket",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "id": self.bucket_name,
                    "name": self.bucket_name,
                    "public": True,
                    "file_size_limit": 52428800,  # 50MB
                    "allowed_mime_types": ["application/pdf", "image/png", "image/jpeg"]
                }
            )
            
            if response.status_code in [200, 201]:
                print(f"   ✅ Created bucket: {self.bucket_name}")
            elif response.status_code == 409:
                print(f"   ℹ️ Bucket already exists: {self.bucket_name}")
            else:
                print(f"   ⚠️ Bucket creation response: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"   ⚠️ Bucket creation error: {e}")
    
    async def list_all_files(self):
        """List all files in storage"""
        print("2. Listing all files in storage...")
        
        try:
            response = await self.client.get(
                f"{SUPABASE_URL}/storage/v1/object/list/{self.bucket_name}",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}"
                }
            )
            
            if response.status_code == 200:
                files = response.json()
                print(f"   Found {len(files)} files:")
                for file in files:
                    name = file.get('name', 'unknown')
                    size = file.get('metadata', {}).get('size', 0)
                    print(f"     - {name} ({size} bytes)")
                return files
            else:
                print(f"   ❌ List files failed: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"   ❌ List files error: {e}")
            return []
    
    async def upload_sample_file(self, filename: str, content: bytes):
        """Upload a file to test storage"""
        print(f"3. Uploading test file: {filename}")
        
        try:
            response = await self.client.post(
                f"{SUPABASE_URL}/storage/v1/object/{self.bucket_name}/{filename}",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/pdf"
                },
                content=content
            )
            
            if response.status_code in [200, 201]:
                print(f"   ✅ Uploaded: {filename}")
                return True
            else:
                print(f"   ❌ Upload failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"   ❌ Upload error: {e}")
            return False
    
    async def fix_document_file_paths(self):
        """Fix file_path in documents table"""
        print("4. Fixing document file paths...")
        
        try:
            # Get all documents with null file_path
            response = await self.client.get(
                f"{SUPABASE_URL}/rest/v1/documents",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}"
                },
                params={"select": "*"}
            )
            
            if response.status_code == 200:
                documents = response.json()
                print(f"   Found {len(documents)} documents to check")
                
                for doc in documents:
                    doc_id = doc.get('id')
                    file_name = doc.get('file_name')
                    file_path = doc.get('file_path')
                    
                    if not file_path and file_name:
                        # Update file_path to be the same as file_name
                        new_file_path = file_name
                        
                        update_response = await self.client.patch(
                            f"{SUPABASE_URL}/rest/v1/documents",
                            headers={
                                "apikey": SUPABASE_KEY,
                                "Authorization": f"Bearer {SUPABASE_KEY}",
                                "Content-Type": "application/json"
                            },
                            params={"id": f"eq.{doc_id}"},
                            json={"file_path": new_file_path}
                        )
                        
                        if update_response.status_code in [200, 204]:
                            print(f"   ✅ Updated {doc_id}: {new_file_path}")
                        else:
                            print(f"   ❌ Update failed for {doc_id}: {update_response.status_code}")
            else:
                print(f"   ❌ Get documents failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Fix file paths error: {e}")

async def main():
    """Fix storage and locate user's PDF"""
    print("PRODUCTION STORAGE SETUP AND FILE RECOVERY")
    print("=" * 50)
    
    async with StorageManager() as storage:
        # Step 1: Create bucket
        await storage.create_bucket_if_not_exists()
        
        # Step 2: List existing files
        files = await storage.list_all_files()
        
        # Step 3: Create sample PDF for testing
        sample_pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n"
        test_filename = "test-invoice.pdf"
        await storage.upload_sample_file(test_filename, sample_pdf_content)
        
        # Step 4: Fix document file paths
        await storage.fix_document_file_paths()
        
        print("\n" + "=" * 50)
        print("STORAGE SETUP COMPLETE")
        
        # Check if user's file exists now
        user_filename = "2025-09-01T10-20 Tax invoice #24347159344967481-24160039583679457.pdf"
        found_user_file = any(f.get('name') == user_filename for f in files)
        
        if found_user_file:
            print(f"✅ Found user's PDF: {user_filename}")
        else:
            print(f"⚠️ User's PDF not found in storage: {user_filename}")
            print("   The file may need to be re-uploaded")

if __name__ == "__main__":
    asyncio.run(main())