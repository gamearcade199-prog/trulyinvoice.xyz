#!/usr/bin/env python
"""Debug invoice extraction to find why invoice_number is missing"""

from app.services.supabase_helper import supabase
import json

print("=" * 80)
print("DEBUGGING INVOICE EXTRACTION")
print("=" * 80)

# Get the latest invoice with raw_extracted_data
result = supabase.table('invoices').select('*').order('created_at', desc=True).limit(1).execute()

if result.data:
    invoice = result.data[0]
    print(f"\n✅ Latest Invoice ID: {invoice.get('id')}")
    print(f"   Vendor: {invoice.get('vendor_name')}")
    print(f"   Invoice Number in DB: {invoice.get('invoice_number')}")
    print(f"   Total: {invoice.get('total_amount')}")
    
    # Check raw_extracted_data
    raw_data = invoice.get('raw_extracted_data')
    if raw_data:
        print(f"\n📊 raw_extracted_data:")
        if isinstance(raw_data, str):
            try:
                raw_data = json.loads(raw_data)
                print(f"   (parsed from JSON string)")
            except Exception as e:
                print(f"   (failed to parse: {e})")
                raw_data = None
        
        if isinstance(raw_data, dict):
            # Show invoice_number related fields
            print(f"\n   🔍 Invoice Number fields:")
            for key in sorted(raw_data.keys()):
                if 'invoice' in key.lower() or 'number' in key.lower():
                    value = raw_data[key]
                    if isinstance(value, str):
                        print(f"      {key}: '{value}'")
                    else:
                        print(f"      {key}: {value}")
            
            # Show all confidence scores
            print(f"\n   📊 Confidence fields:")
            for key in sorted(raw_data.keys()):
                if 'confidence' in key.lower():
                    print(f"      {key}: {raw_data[key]}")
            
            # Show a sample of other fields
            print(f"\n   📋 Other key fields:")
            for key in ['vendor_name', 'invoice_date', 'total_amount', 'payment_status']:
                if key in raw_data:
                    print(f"      {key}: {raw_data[key]}")
    else:
        print("\n   ❌ No raw_extracted_data found!")

else:
    print("❌ No invoices found")
