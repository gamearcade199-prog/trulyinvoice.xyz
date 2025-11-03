"""
Quick check of invoice amounts in database
"""
from supabase import create_client
import os
from dotenv import load_dotenv
import json

load_dotenv()

supabase = create_client(
    "https://ldvwxqluaheuhbycdpwn.supabase.co",
    os.getenv("SUPABASE_SERVICE_KEY")
)

# Get the latest invoice
result = supabase.table('invoices').select(
    'id,invoice_number,vendor_name,total_amount,subtotal,tax_amount,line_items,is_consolidated,sub_vendor_count'
).eq('id', '85ffd7c1-7e7d-4508-9529-f0c169181fd4').single().execute()

print("\n" + "="*80)
print("📊 INVOICE DATABASE CHECK")
print("="*80)

invoice = result.data
print(f"\n📄 Invoice: {invoice['invoice_number']}")
print(f"🏢 Vendor: {invoice['vendor_name']}")
print(f"💰 Total Amount: ₹{invoice['total_amount']}")
print(f"📦 Subtotal: ₹{invoice.get('subtotal', 0)}")
print(f"📊 Tax: ₹{invoice.get('tax_amount', 0)}")
print(f"🔄 Consolidated: {invoice.get('is_consolidated', False)}")
print(f"👥 Sub-Vendors: {invoice.get('sub_vendor_count', 0)}")

# Check line items
line_items = invoice.get('line_items', [])
print(f"\n📋 Line Items: {len(line_items)} items")

if line_items:
    print("\nFirst 3 line items:")
    for idx, item in enumerate(line_items[:3], 1):
        print(f"\n  {idx}. {item.get('description', 'N/A')}")
        print(f"     Amount: ₹{item.get('amount', 0)}")
        print(f"     Sub-Vendor: {item.get('sub_vendor', 'N/A')}")
        print(f"     Sub-Bill: {item.get('sub_bill_number', 'N/A')}")

print("\n" + "="*80)
