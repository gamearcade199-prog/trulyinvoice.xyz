"""
Check database data quality for vendor_gstin
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.supabase_helper import supabase

print("="*80)
print("DATABASE DATA QUALITY CHECK: vendor_gstin")
print("="*80)

# Count total invoices
response = supabase.table('invoices').select('id', count='exact').execute()
total_invoices = response.count if response.count else 0

# Count invoices with vendor_gstin
response = supabase.table('invoices').select('vendor_gstin').not_.is_('vendor_gstin', 'null').execute()
with_vendor_gstin = len(response.data) if response.data else 0

# Count invoices with customer_gstin
response = supabase.table('invoices').select('customer_gstin').not_.is_('customer_gstin', 'null').execute()
with_customer_gstin = len(response.data) if response.data else 0

print(f"\n📊 Statistics:")
print(f"   Total Invoices: {total_invoices}")
print(f"   With Vendor GSTIN: {with_vendor_gstin} ({with_vendor_gstin/total_invoices*100:.1f}% if total_invoices else 0)" if total_invoices > 0 else "")
print(f"   With Customer GSTIN: {with_customer_gstin} ({with_customer_gstin/total_invoices*100:.1f}%)" if total_invoices > 0 else "")

print(f"\n❌ Missing Vendor GSTIN: {total_invoices - with_vendor_gstin} ({(total_invoices-with_vendor_gstin)/total_invoices*100:.1f}%)" if total_invoices > 0 else "")

# Sample invoices with GSTIN
print(f"\n📋 Sample Invoices WITH vendor_gstin:")
response = supabase.table('invoices').select('invoice_number, vendor_name, vendor_gstin').not_.is_('vendor_gstin', 'null').limit(5).execute()

if response.data:
    for inv in response.data:
        print(f"   {inv['invoice_number']}: {inv['vendor_name'][:40]} - GSTIN: {inv['vendor_gstin']}")
else:
    print("   ❌ No invoices with vendor_gstin found!")

# Sample invoices WITHOUT GSTIN
print(f"\n📋 Sample Invoices WITHOUT vendor_gstin:")
response = supabase.table('invoices').select('invoice_number, vendor_name, vendor_gstin').is_('vendor_gstin', 'null').limit(5).execute()

if response.data:
    for inv in response.data:
        print(f"   {inv['invoice_number']}: {inv['vendor_name'][:40] if inv['vendor_name'] else 'No name'} - GSTIN: NULL")
else:
    print("   ✅ All invoices have vendor_gstin!")

print("\n" + "="*80)
print("CONCLUSION:")
print("="*80)

if total_invoices > 0:
    if with_vendor_gstin == 0:
        print("\n❌ CRITICAL: 0% of invoices have vendor_gstin!")
        print("   → OCR extraction is NOT working for GSTIN")
        print("   → Fix backend/app/services/invoice.py extraction logic")
    elif with_vendor_gstin < total_invoices * 0.5:
        print(f"\n⚠️ WARNING: Only {with_vendor_gstin/total_invoices*100:.1f}% have vendor_gstin")
        print("   → OCR extraction needs improvement")
        print("   → Check GSTIN regex patterns and field mapping")
    elif with_vendor_gstin < total_invoices * 0.9:
        print(f"\n⚠️ MODERATE: {with_vendor_gstin/total_invoices*100:.1f}% have vendor_gstin")
        print("   → Most invoices OK, but some missing")
        print("   → May be invoice format variations")
    else:
        print(f"\n✅ GOOD: {with_vendor_gstin/total_invoices*100:.1f}% have vendor_gstin")
        print("   → OCR extraction is working well")
else:
    print("\n⚠️ No invoices in database")
