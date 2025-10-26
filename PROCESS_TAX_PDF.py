"""
Process ONLY the tax.pdf document with AI extraction
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

print("🔍 Finding tax.pdf document...\n")

# Get tax.pdf document
url = f"{SUPABASE_URL}/rest/v1/documents?file_name=eq.tax.pdf"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    documents = response.json()
    
    if documents and len(documents) > 0:
        doc = documents[0]
        doc_id = doc['id']
        
        print(f"📄 Found: {doc['file_name']}")
        print(f"   ID: {doc_id}")
        print(f"   Status: {doc['status']}\n")
        
        # Process it
        print("🤖 Processing with AI extraction...")
        process_url = f"http://localhost:8000/api/documents/{doc_id}/process"
        process_response = requests.post(process_url)
        
        if process_response.status_code == 200:
            result = process_response.json()
            print("\n✅ SUCCESS! Invoice created with REAL values:\n")
            print(f"   Vendor: {result.get('vendor_name')}")
            print(f"   Invoice #: {result.get('invoice_id')}")
            print(f"   Total: ₹{result.get('total_amount'):,.2f}")
            print("\n🎉 Check the database to see the correct values!")
        else:
            print(f"\n❌ Error: {process_response.status_code}")
            print(f"   {process_response.text}")
    else:
        print("❌ tax.pdf not found in database")
else:
    print(f"❌ Error fetching documents: {response.status_code}")
