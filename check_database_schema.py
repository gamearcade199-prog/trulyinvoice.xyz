"""
Check current database schema for invoices table
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.supabase_helper import supabase

print("="*80)
print("DATABASE SCHEMA CHECK: invoices table")
print("="*80)

# Get schema from information_schema
query = """
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'invoices' 
ORDER BY ordinal_position;
"""

try:
    # Execute raw SQL query
    response = supabase.rpc('exec_sql', {'query': query}).execute()
    
    if response.data:
        print(f"\n📋 Current Schema ({len(response.data)} columns):\n")
        
        for col in response.data:
            nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
            max_len = f"({col['character_maximum_length']})" if col['character_maximum_length'] else ""
            print(f"   {col['column_name']:<30} {col['data_type']}{max_len:<15} {nullable}")
        
        # Check for missing critical fields
        current_columns = [col['column_name'] for col in response.data]
        
        critical_fields = [
            'vendor_gstin', 'customer_gstin',
            'vendor_pan', 'customer_pan',
            'vendor_phone', 'customer_phone',
            'vendor_email', 'customer_email',
            'vendor_state', 'customer_state',
            'po_number', 'reference_number',
            'payment_method', 'payment_terms',
            'bank_account', 'bank_name', 'bank_ifsc'
        ]
        
        missing = [field for field in critical_fields if field not in current_columns]
        present = [field for field in critical_fields if field in current_columns]
        
        print(f"\n✅ Present Critical Fields ({len(present)}/{len(critical_fields)}):")
        for field in present:
            print(f"   ✓ {field}")
        
        if missing:
            print(f"\n❌ Missing Critical Fields ({len(missing)}):")
            for field in missing:
                print(f"   ✗ {field}")
        else:
            print(f"\n🎉 ALL critical fields present!")
            
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTrying direct table query instead...")
    
    # Fallback: Get sample row to see columns
    response = supabase.table('invoices').select('*').limit(1).execute()
    
    if response.data:
        columns = list(response.data[0].keys())
        print(f"\n📋 Columns from sample row ({len(columns)} total):\n")
        
        for col in sorted(columns):
            print(f"   {col}")
        
        # Check for missing fields
        critical_fields = [
            'vendor_gstin', 'customer_gstin',
            'vendor_pan', 'customer_pan',
            'vendor_phone', 'customer_phone',
            'vendor_email', 'customer_email',
            'vendor_state', 'customer_state',
            'po_number', 'reference_number',
            'payment_method', 'payment_terms',
            'bank_account'
        ]
        
        missing = [field for field in critical_fields if field not in columns]
        present = [field for field in critical_fields if field in columns]
        
        print(f"\n✅ Present Critical Fields ({len(present)}/{len(critical_fields)}):")
        for field in present:
            print(f"   ✓ {field}")
        
        if missing:
            print(f"\n❌ Missing Critical Fields ({len(missing)}):")
            for field in missing:
                print(f"   ✗ {field}")
            
            print(f"\n📝 SQL to add missing columns:")
            print("ALTER TABLE invoices")
            for i, field in enumerate(missing):
                comma = "," if i < len(missing) - 1 else ";"
                if 'email' in field:
                    print(f"ADD COLUMN IF NOT EXISTS {field} VARCHAR(255){comma}")
                elif 'phone' in field:
                    print(f"ADD COLUMN IF NOT EXISTS {field} VARCHAR(15){comma}")
                elif field in ['vendor_gstin', 'customer_gstin']:
                    print(f"ADD COLUMN IF NOT EXISTS {field} VARCHAR(15){comma}")
                elif field in ['vendor_pan', 'customer_pan']:
                    print(f"ADD COLUMN IF NOT EXISTS {field} VARCHAR(10){comma}")
                else:
                    print(f"ADD COLUMN IF NOT EXISTS {field} TEXT{comma}")
        else:
            print(f"\n🎉 ALL critical fields present!")
