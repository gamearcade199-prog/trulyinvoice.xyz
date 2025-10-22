#!/usr/bin/env python
"""Fix invoices with missing invoice_number"""

from app.services.supabase_helper import supabase

print("=" * 80)
print("FIXING INVOICES WITH MISSING INVOICE_NUMBER")
print("=" * 80)

# Get invoices with missing invoice_number
result = supabase.table('invoices').select('*').is_('invoice_number', 'NULL').execute()

if result.data:
    print(f"\n✅ Found {len(result.data)} invoices with missing invoice_number\n")
    
    for idx, invoice in enumerate(result.data, 1):
        invoice_id = invoice.get('id')
        document_id = invoice.get('document_id')
        vendor = invoice.get('vendor_name') or 'Unknown'
        
        # Generate invoice_number from document_id
        fallback_inv_num = f"INV-{document_id[:8].upper()}" if document_id else f"INV-{idx:06d}"
        
        print(f"{idx}. Fixing: {str(vendor):30} | New Inv#: {fallback_inv_num}")
        
        # Update the invoice
        update_result = supabase.table('invoices').update({
            'invoice_number': fallback_inv_num
        }).eq('id', invoice_id).execute()
        
        if update_result.data:
            print(f"   ✅ Updated successfully")
        else:
            print(f"   ❌ Failed to update!")
    
    print(f"\n✅ Fixed {len(result.data)} invoices!")
    
else:
    print("\n✅ No invoices with missing invoice_number found!")
