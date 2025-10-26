#!/usr/bin/env python
"""Comprehensive audit of invoice data quality"""

from app.services.supabase_helper import supabase

print("=" * 80)
print("COMPREHENSIVE INVOICE DATA QUALITY AUDIT")
print("=" * 80)

# Get last 10 invoices
result = supabase.table('invoices').select('*').order('created_at', desc=True).limit(10).execute()

if result.data:
    print(f"\n✅ Found {len(result.data)} invoices\n")
    
    # Audit each invoice
    issues = []
    for idx, invoice in enumerate(result.data, 1):
        invoice_id = invoice.get('id')[:8]
        vendor = invoice.get('vendor_name') or 'MISSING'
        inv_num = invoice.get('invoice_number') or 'MISSING'
        total = invoice.get('total_amount')
        
        print(f"{idx}. ID: {invoice_id} | Vendor: {vendor:25} | Inv#: {inv_num:15} | Total: {total}")
        
        # Check for common issues
        if not invoice.get('invoice_number') or invoice.get('invoice_number') == '':
            issues.append(f"Invoice {idx}: Empty invoice_number")
        
        if not invoice.get('vendor_name'):
            issues.append(f"Invoice {idx}: Missing vendor_name")
        
        if not invoice.get('total_amount') or invoice.get('total_amount') == 0:
            issues.append(f"Invoice {idx}: Zero or missing total_amount")
        
        if not invoice.get('invoice_date'):
            issues.append(f"Invoice {idx}: Missing invoice_date")
        
        if not invoice.get('payment_status'):
            issues.append(f"Invoice {idx}: Missing payment_status")
            
        # Check for unusual values
        confidence = invoice.get('confidence_score')
        if confidence and (confidence < 0.5 or confidence > 1.0):
            issues.append(f"Invoice {idx}: Invalid confidence_score {confidence}")
    
    if issues:
        print(f"\n⚠️  ISSUES FOUND:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print(f"\n✅ NO CRITICAL ISSUES FOUND")
    
    # Summary stats
    print(f"\n📊 SUMMARY:")
    print(f"   Invoices with vendor_name: {sum(1 for i in result.data if i.get('vendor_name'))}")
    print(f"   Invoices with invoice_number: {sum(1 for i in result.data if i.get('invoice_number'))}")
    print(f"   Invoices with total > 0: {sum(1 for i in result.data if i.get('total_amount', 0) > 0)}")
    print(f"   Invoices with invoice_date: {sum(1 for i in result.data if i.get('invoice_date'))}")
    
else:
    print("❌ No invoices found")
