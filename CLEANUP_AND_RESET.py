"""
Delete all invoices and reset documents to re-process with correct numbers
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Prefer": "return=representation"
}

print("🗑️ Cleaning up incorrect invoices...\n")

# 1. Get all invoices
invoices_url = f"{SUPABASE_URL}/rest/v1/invoices"
response = requests.get(invoices_url, headers=headers)

if response.status_code == 200:
    invoices = response.json()
    print(f"Found {len(invoices)} invoices to delete\n")
    
    # Delete each invoice individually
    deleted_count = 0
    for invoice in invoices:
        invoice_id = invoice['id']
        delete_url = f"{SUPABASE_URL}/rest/v1/invoices?id=eq.{invoice_id}"
        delete_response = requests.delete(delete_url, headers=headers)
        
        if delete_response.status_code in [200, 204]:
            deleted_count += 1
        else:
            print(f"❌ Error deleting {invoice_id}: {delete_response.text}")
    
    print(f"✅ Deleted {deleted_count}/{len(invoices)} invoices")
else:
    print(f"❌ Error fetching invoices: {response.text}")

# 2. Reset document status to 'uploaded'
print("\n🔄 Resetting document status to 'uploaded'...\n")

docs_url = f"{SUPABASE_URL}/rest/v1/documents?status=eq.completed"
reset_data = {"status": "uploaded"}
reset_response = requests.patch(docs_url, headers=headers, json=reset_data)

if reset_response.status_code == 200:
    updated_docs = reset_response.json()
    print(f"✅ Reset {len(updated_docs)} documents to 'uploaded' status")
else:
    print(f"❌ Error resetting: {reset_response.text}")

print("\n" + "=" * 60)
print("✅ Cleanup complete! Ready to re-process with correct extraction")
print("=" * 60)
print("\nRun: python PROCESS_ALL_DOCUMENTS.py")
