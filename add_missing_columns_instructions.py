"""
Add missing columns to invoices table via Supabase SQL API
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.supabase_helper import supabase
import requests

print("="*80)
print("🔧 ADDING MISSING COLUMNS TO INVOICES TABLE")
print("="*80)

# List of columns to add
missing_columns = [
    ('paid_amount', 'DECIMAL(15, 2)', 'Amount already paid towards this invoice'),
    ('balance', 'DECIMAL(15, 2)', 'Balance/remaining amount to be paid'),
    ('balance_due', 'DECIMAL(15, 2)', 'Amount due/outstanding'),
    ('invoice_amount_in_words', 'TEXT', 'Total amount in words'),
    ('irn_number', 'VARCHAR(100)', 'Invoice Reference Number (IRN) for GST'),
    ('round_off', 'DECIMAL(10, 2)', 'Round off adjustment amount'),
    ('eway_bill', 'VARCHAR(100)', 'E-way bill number (alternative field)'),
]

print("\n📝 Columns to add:")
for col_name, col_type, col_desc in missing_columns:
    print(f"  - {col_name:30s} {col_type:20s} - {col_desc}")

print("\n" + "="*80)
print("⚠️  IMPORTANT: You need to add these columns via Supabase Dashboard")
print("="*80)

print("\n📋 INSTRUCTIONS:")
print("\n1. Go to: https://supabase.com/dashboard/project/ldvwxqluaheuhbycdpwn/editor")
print("\n2. Click 'SQL Editor' in the left sidebar")
print("\n3. Click 'New Query' button")
print("\n4. Copy and paste this SQL:\n")

print("-" * 80)
print("""
-- Add missing columns to invoices table
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS paid_amount DECIMAL(15, 2);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS balance DECIMAL(15, 2);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS balance_due DECIMAL(15, 2);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS invoice_amount_in_words TEXT;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS irn_number VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS round_off DECIMAL(10, 2);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS eway_bill VARCHAR(100);

-- Add comments
COMMENT ON COLUMN invoices.paid_amount IS 'Amount already paid';
COMMENT ON COLUMN invoices.balance IS 'Balance remaining';
COMMENT ON COLUMN invoices.balance_due IS 'Amount due';
COMMENT ON COLUMN invoices.invoice_amount_in_words IS 'Amount in words';
COMMENT ON COLUMN invoices.irn_number IS 'GST IRN number';
COMMENT ON COLUMN invoices.round_off IS 'Round off amount';
COMMENT ON COLUMN invoices.eway_bill IS 'E-way bill number';

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_invoices_irn_number ON invoices(irn_number);
CREATE INDEX IF NOT EXISTS idx_invoices_balance_due ON invoices(balance_due) WHERE balance_due > 0;
""")
print("-" * 80)

print("\n5. Click 'Run' button (or press Ctrl+Enter)")
print("\n6. You should see: 'Success. No rows returned'")
print("\n7. Come back here and upload the invoice again!")

print("\n" + "="*80)
print("📊 ALTERNATIVE: Use Supabase Table Editor (Easier!)")
print("="*80)

print("\n1. Go to: https://supabase.com/dashboard/project/ldvwxqluaheuhbycdpwn/editor")
print("\n2. Click on 'invoices' table")
print("\n3. Click the '+' button next to columns")
print("\n4. Add each column manually:")

for col_name, col_type, col_desc in missing_columns:
    col_type_ui = col_type.replace('DECIMAL(15, 2)', 'numeric').replace('DECIMAL(10, 2)', 'numeric').replace('TEXT', 'text').replace('VARCHAR(100)', 'varchar')
    print(f"\n   Column: {col_name}")
    print(f"   Type:   {col_type_ui}")
    print(f"   Desc:   {col_desc}")
    print(f"   Nullable: YES")
    print(f"   Default: NULL")

print("\n" + "="*80)
print("✅ AFTER ADDING COLUMNS:")
print("="*80)

print("\n1. Backend will auto-reload (watch terminal)")
print("2. Upload the invoice again via http://localhost:3000")
print("3. It should save successfully!")
print("4. Run: python test_enhanced_extraction.py to verify")

print("\n" + "="*80)
