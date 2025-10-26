"""
Quick script to manually process an existing invoice document
This will trigger the AI extraction for documents showing ₹0
"""

import requests
import json

# Configuration
API_URL = "http://localhost:8000"
DOCUMENT_ID = 1  # Change this to your document ID

# You'll need your access token - get it from browser console
# In browser console, run: (await supabase.auth.getSession()).data.session.access_token
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE"

def process_document(doc_id: int, access_token: str):
    """Process a document via the API"""
    
    url = f"{API_URL}/api/documents/{doc_id}/process"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    print(f"Processing document {doc_id}...")
    print(f"URL: {url}")
    
    try:
        response = requests.post(url, headers=headers)
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("\n✅ Document processed successfully!")
            print("Refresh your invoices page to see the extracted data.")
        else:
            print(f"\n❌ Error processing document")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    print("=" * 60)
    print("TrulyInvoice - Manual Document Processing")
    print("=" * 60)
    
    if ACCESS_TOKEN == "YOUR_ACCESS_TOKEN_HERE":
        print("\n⚠️  Please update ACCESS_TOKEN in this script!")
        print("\nSteps to get your access token:")
        print("1. Open browser console (F12)")
        print("2. Go to Console tab")
        print("3. Run this command:")
        print("   (await supabase.auth.getSession()).data.session.access_token")
        print("4. Copy the token and paste it in this script")
        print("\nOr just re-upload the invoice - backend will auto-process it!")
    else:
        process_document(DOCUMENT_ID, ACCESS_TOKEN)
