"""
Deep check: Compare AI extracted fields vs actual database columns
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.supabase_helper import supabase

print("="*80)
print("🔍 DEEP CHECK: AI EXTRACTED FIELDS vs DATABASE COLUMNS")
print("="*80)

# Get actual database columns
print("\n📊 Step 1: Getting actual database columns...")
response = supabase.table('invoices').select('*').limit(1).execute()
if response.data:
    db_columns = set(response.data[0].keys())
    print(f"✅ Found {len(db_columns)} columns in database")
else:
    print("❌ No data in database")
    sys.exit(1)

# List of ALL fields that AI might extract (from the logs you provided)
ai_extracted_fields = {
    # Core invoice fields
    'invoice_number', 'invoice_date', 'due_date', 'invoice_type',
    'po_number', 'reference_number', 'order_number', 'order_date',
    
    # Vendor fields
    'vendor_name', 'vendor_address', 'vendor_state', 'vendor_pincode',
    'vendor_phone', 'vendor_email', 'vendor_gstin', 'vendor_pan', 
    'vendor_tan', 'vendor_cin', 'vendor_type',
    
    # Customer fields
    'customer_name', 'customer_address', 'customer_state', 'customer_pincode',
    'customer_phone', 'customer_email', 'customer_gstin', 'customer_pan',
    'customer_po', 'customer_po_number',
    
    # Shipping fields
    'ship_to_customer_name', 'ship_to_customer_address', 
    'ship_to_customer_state', 'ship_to_customer_phone',
    'customer_gstin_ship_to', 'shipping_address', 'billing_address',
    
    # Financial fields
    'subtotal', 'discount', 'discount_percentage', 'shipping_charges',
    'cgst', 'sgst', 'igst', 'cess', 'vat', 'ugst',
    'total_amount', 'paid_amount', 'balance', 'balance_due',
    'taxable_amount', 'taxable_value', 'tax_amount', 'total_gst',
    'round_off', 'roundoff',
    
    # Payment fields
    'payment_status', 'payment_method', 'payment_terms', 'payment_date',
    'payment_reference', 'currency',
    
    # Banking fields
    'bank_name', 'bank_account', 'account_number', 'ifsc_code', 'swift_code',
    
    # Line items
    'line_items',
    
    # Transport/Logistics
    'eway_bill', 'eway_bill_number', 'eway_bill_date', 'eway_bill_time',
    'vehicle_number', 'vehicle_registration_number', 'driver_name',
    'lr_number', 'lr_rr_number', 'lr_rr_date',
    'transporter_name', 'mode_of_transport', 'freight',
    'delivery_number', 'delivery_date', 'delivery_note',
    'tracking_number', 'distance_km',
    
    # Compliance
    'irn_number', 'place_of_supply', 'supplying_state', 'reverse_charge',
    'hsn_code', 'sac_code',
    
    # Additional
    'notes', 'terms', 'invoice_amount_in_words', 'invoice_value_in_words',
    'mrp_per_bag', 'tags', 'category_id',
    
    # Timestamps
    'created_at', 'updated_at'
}

print(f"\n🤖 AI can extract: {len(ai_extracted_fields)} fields")

# Find missing columns
missing_columns = ai_extracted_fields - db_columns
existing_columns = ai_extracted_fields & db_columns

print("\n" + "="*80)
print("ANALYSIS RESULTS:")
print("="*80)

print(f"\n✅ EXISTING in DB: {len(existing_columns)} fields")
for col in sorted(existing_columns):
    print(f"   ✅ {col}")

print(f"\n❌ MISSING from DB: {len(missing_columns)} fields")
for col in sorted(missing_columns):
    print(f"   ❌ {col}")

print("\n" + "="*80)
print("SQL TO ADD MISSING COLUMNS:")
print("="*80)

# Generate SQL for missing columns
field_types = {
    # Text fields
    'customer_email': 'VARCHAR(255)',
    'vendor_cin': 'VARCHAR(50)',
    'customer_po': 'VARCHAR(100)',
    'customer_po_number': 'VARCHAR(100)',
    'ship_to_customer_name': 'VARCHAR(255)',
    'ship_to_customer_address': 'TEXT',
    'ship_to_customer_state': 'VARCHAR(100)',
    'ship_to_customer_phone': 'VARCHAR(20)',
    'customer_gstin_ship_to': 'VARCHAR(15)',
    'shipping_address': 'TEXT',
    'billing_address': 'TEXT',
    'balance': 'DECIMAL(15, 2)',
    'balance_due': 'DECIMAL(15, 2)',
    'paid_amount': 'DECIMAL(15, 2)',
    'round_off': 'DECIMAL(10, 2)',
    'roundoff': 'DECIMAL(10, 2)',
    'irn_number': 'VARCHAR(100)',
    'eway_bill': 'VARCHAR(100)',
    'eway_bill_date': 'DATE',
    'eway_bill_time': 'TIME',
    'vehicle_registration_number': 'VARCHAR(50)',
    'mode_of_transport': 'VARCHAR(50)',
    'invoice_amount_in_words': 'TEXT',
    'invoice_value_in_words': 'TEXT',
    'mrp_per_bag': 'DECIMAL(10, 2)',
    'lr_rr_number': 'VARCHAR(50)',
    'lr_rr_date': 'DATE',
    'delivery_note': 'TEXT',
    'supplying_state': 'VARCHAR(100)',
    'terms': 'TEXT',
    'due_date': 'DATE',
}

print("\n-- Copy and paste this into Supabase SQL Editor:\n")
for col in sorted(missing_columns):
    col_type = field_types.get(col, 'TEXT')
    print(f"ALTER TABLE invoices ADD COLUMN IF NOT EXISTS {col} {col_type};")

print("\n-- Create indexes for important fields:")
print("CREATE INDEX IF NOT EXISTS idx_invoices_customer_email ON invoices(customer_email);")
print("CREATE INDEX IF NOT EXISTS idx_invoices_irn_number ON invoices(irn_number);")
print("CREATE INDEX IF NOT EXISTS idx_invoices_eway_bill_number ON invoices(eway_bill_number);")
print("CREATE INDEX IF NOT EXISTS idx_invoices_balance_due ON invoices(balance_due) WHERE balance_due > 0;")

print("\n" + "="*80)
print("CRITICAL MISSING COLUMNS (High Priority):")
print("="*80)

critical_columns = {
    'customer_email', 'balance', 'balance_due', 'paid_amount',
    'irn_number', 'eway_bill', 'invoice_amount_in_words', 'round_off'
}

critical_missing = missing_columns & critical_columns
print(f"\n🚨 {len(critical_missing)} CRITICAL columns missing:")
for col in sorted(critical_missing):
    print(f"   🚨 {col}")

print("\n" + "="*80)
print("QUICK FIX SQL (Critical columns only):")
print("="*80)
print("\n-- Add these ASAP to make invoices save:\n")
for col in sorted(critical_missing):
    col_type = field_types.get(col, 'TEXT')
    print(f"ALTER TABLE invoices ADD COLUMN IF NOT EXISTS {col} {col_type};")

print("\n" + "="*80)
