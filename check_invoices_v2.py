"""
Check invoices in database - uses requests (no httpx conflicts!)
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

print("=" * 60)
print(" INVOICE DATABASE STATUS")
print("=" * 60)
print()

# Get invoices
invoices_url = f"{SUPABASE_URL}/rest/v1/invoices?order=created_at.desc"
response = requests.get(invoices_url, headers=headers)

if response.status_code == 200:
    invoices = response.json()
    print(f"✅ Total Invoices in Database: {len(invoices)}")
    print()
    
    if invoices:
        print("📊 Recent Invoices:")
        print("-" * 60)
        for inv in invoices[:10]:  # Show first 10
            vendor = inv.get('vendor_name', 'N/A')
            amount = inv.get('total_amount', 0)
            inv_num = inv.get('invoice_number', 'N/A')
            status = inv.get('payment_status', 'unknown')
            
            print(f"  • {vendor[:40]}")
            print(f"    Invoice #: {inv_num}")
            print(f"    Amount: ₹{amount:,.2f}")
            print(f"    Status: {status}")
            print()
    else:
        print("  No invoices found.")
else:
    print(f"❌ Error fetching invoices: {response.status_code}")
    print(f"   {response.text}")

print()

# Get documents
docs_url = f"{SUPABASE_URL}/rest/v1/documents?order=created_at.desc&limit=10"
doc_response = requests.get(docs_url, headers=headers)

if doc_response.status_code == 200:
    documents = doc_response.json()
    print(f"📄 Total Documents: {len(documents)} (showing latest)")
    print()
    
    status_counts = {}
    for doc in documents:
        status = doc.get('status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("Document Status Breakdown:")
    for status, count in status_counts.items():
        print(f"  • {status}: {count}")

print()
print("=" * 60)
print("✅ Check complete!")
print("=" * 60)
