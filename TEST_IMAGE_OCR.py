"""
Test IMAGE OCR processing with optimized system
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

print("🔍 Finding IMAGE documents (JPG/PNG)...\n")

# Get image documents
url = f"{SUPABASE_URL}/rest/v1/documents?file_name=like.%25.jpg&select=*"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    documents = response.json()
    
    if documents and len(documents) > 0:
        print(f"📸 Found {len(documents)} image document(s)\n")
        
        # Take the first one
        doc = documents[0]
        doc_id = doc['id']
        
        print(f"   File: {doc['file_name']}")
        print(f"   ID: {doc_id}")
        print(f"   Status: {doc['status']}")
        print(f"\n🤖 Processing with NEW IMAGE OCR...\n")
        
        # Process it
        process_url = f"http://localhost:8000/api/documents/{doc_id}/process"
        process_response = requests.post(process_url)
        
        if process_response.status_code == 200:
            result = process_response.json()
            print("✅ SUCCESS! Image invoice processed with OCR:\n")
            print(f"   Vendor: {result.get('vendor_name')}")
            print(f"   Invoice #: {result.get('invoice_id')}")
            print(f"   Total: ₹{result.get('total_amount'):,.2f}")
            print("\n🎉 IMAGE OCR WORKING! Check if values are real (not ₹0 or ₹11,800)")
        else:
            print(f"\n❌ Error: {process_response.status_code}")
            print(f"   {process_response.text}")
    else:
        print("ℹ️ No JPG images found. Trying PNG...")
        
        url = f"{SUPABASE_URL}/rest/v1/documents?file_name=like.%25.png&select=*"
        response = requests.get(url, headers=headers)
        documents = response.json() if response.status_code == 200 else []
        
        if documents:
            print(f"📸 Found {len(documents)} PNG document(s)")
            print("   (Process same as JPG)")
        else:
            print("ℹ️ No image documents found. Upload a JPG/PNG to test OCR!")
else:
    print(f"❌ Error fetching documents: {response.status_code}")
