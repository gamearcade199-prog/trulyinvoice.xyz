"""
Process all pending documents and create invoices
Works with the NEW clean backend architecture
"""
import requests
import os
from dotenv import load_dotenv

# Load .env from backend directory
load_dotenv('backend/.env')

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

print(f"🔗 Supabase URL: {SUPABASE_URL[:30] if SUPABASE_URL else 'NOT FOUND'}...")
print(f"🔑 API Key: {'✅ Loaded' if SUPABASE_KEY else '❌ Missing'}")

def get_pending_documents():
    """Get all documents with status='uploaded'"""
    url = f"{SUPABASE_URL}/rest/v1/documents?status=eq.uploaded"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    
    response = requests.get(url, headers=headers)
    return response.json()

def process_document(doc_id):
    """Trigger backend processing for a document"""
    url = f"http://localhost:8000/api/documents/{doc_id}/process"
    response = requests.post(url)
    return response.json()

if __name__ == "__main__":
    print("🔍 Checking for pending documents...")
    
    documents = get_pending_documents()
    print(f"✅ Found {len(documents)} documents to process\n")
    
    for doc in documents:
        doc_id = doc['id']
        file_name = doc.get('file_name', 'Unknown')
        
        print(f"📄 Processing: {file_name}")
        print(f"   ID: {doc_id}")
        
        try:
            result = process_document(doc_id)
            print(f"   📊 Response: {result}")
            if result.get('success'):
                print(f"   ✅ Created invoice #{result.get('invoice_number')}")
                print(f"   💰 Amount: ₹{result.get('total_amount')}")
            else:
                print(f"   ❌ Failed: {result.get('message', 'Unknown error')}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    print(f"🎉 Processed {len(documents)} documents!")
    print("🔄 Refresh your browser to see the invoices!")
