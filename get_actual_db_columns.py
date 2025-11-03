"""
Get ACTUAL columns from Supabase invoices table
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.supabase_helper import supabase

print("="*80)
print("📊 GETTING ACTUAL DATABASE COLUMNS FROM SUPABASE")
print("="*80)

# Try to insert a dummy invoice with ALL possible fields to see which ones are rejected
test_fields = {
    'invoice_number': 'TEST',
    'vendor_name': 'TEST',
    'customer_name': 'TEST',
    'total_amount': 0,
    'paid_amount': 0,
    'balance': 0,
    'balance_due': 0,
    'invoice_amount_in_words': 'TEST',
    'irn_number': 'TEST',
    'round_off': 0,
    'eway_bill': 'TEST',
    'eway_bill_number': 'TEST'
}

print("\n🧪 Testing which fields exist in database...")
print(f"Testing fields: {list(test_fields.keys())}")

# Query an existing invoice to see all columns
try:
    response = supabase.table('invoices').select('*').limit(1).execute()
    if response.data:
        actual_columns = list(response.data[0].keys())
        print(f"\n✅ Found {len(actual_columns)} columns in invoices table:")
        print("\nColumns:")
        for col in sorted(actual_columns):
            print(f"  - {col}")
        
        # Check which test fields exist
        print("\n" + "="*80)
        print("FIELD EXISTENCE CHECK:")
        print("="*80)
        
        missing_fields = []
        existing_fields = []
        
        for field in test_fields.keys():
            if field in actual_columns:
                print(f"  ✅ {field:30s} EXISTS")
                existing_fields.append(field)
            else:
                print(f"  ❌ {field:30s} MISSING")
                missing_fields.append(field)
        
        print("\n" + "="*80)
        print("SUMMARY:")
        print("="*80)
        print(f"\n✅ Existing: {len(existing_fields)} fields")
        print(f"   {existing_fields}")
        
        print(f"\n❌ Missing: {len(missing_fields)} fields")
        print(f"   {missing_fields}")
        
        print("\n" + "="*80)
        print("CODE TO ADD TO documents.py:")
        print("="*80)
        print("\nexcluded_fields = {")
        print("    'error', 'error_message', '_extraction_metadata',")
        for field in missing_fields:
            print(f"    '{field}',")
        print("}")
        
    else:
        print("❌ No invoices found in database")
except Exception as e:
    print(f"❌ Error: {e}")
