#!/usr/bin/env python
"""Check invoice structure and data quality"""

from app.services.supabase_helper import supabase
import json

print("=" * 60)
print("CHECKING INVOICE DATA STRUCTURE")
print("=" * 60)

# Get the most recent invoice
result = supabase.table('invoices').select('*').order('created_at', desc=True).limit(1).execute()

if result.data:
    invoice = result.data[0]
    print("\n✅ Latest Invoice:")
    print(f"  id (UUID): {invoice.get('id')}")
    print(f"  invoice_number: {invoice.get('invoice_number')}")
    print(f"  vendor_name: {invoice.get('vendor_name')}")
    print(f"  invoice_date: {invoice.get('invoice_date')}")
    print(f"  total_amount: {invoice.get('total_amount')}")
    
    # Check raw_extracted_data
    raw_data = invoice.get('raw_extracted_data')
    if raw_data:
        print(f"\n  raw_extracted_data type: {type(raw_data).__name__}")
        if isinstance(raw_data, str):
            try:
                raw_data = json.loads(raw_data)
                print(f"    (parsed from JSON string)")
            except:
                print(f"    (failed to parse JSON)")
        
        if isinstance(raw_data, dict):
            print(f"    Sample keys: {list(raw_data.keys())[:15]}")
            if 'invoice_number' in raw_data:
                print(f"    invoice_number in raw_data: {raw_data['invoice_number']}")
            if 'vendor_name' in raw_data:
                print(f"    vendor_name in raw_data: {raw_data['vendor_name']}")
    
    print("\n  All non-null fields:")
    for key, value in invoice.items():
        if value is not None and key not in ['id', 'user_id', 'raw_extracted_data']:
            print(f"    {key}: {str(value)[:80]}")

else:
    print("❌ No invoices found")
