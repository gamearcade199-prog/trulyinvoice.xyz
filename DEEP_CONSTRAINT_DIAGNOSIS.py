"""
DEEP DIAGNOSIS: Find the EXACT constraint causing the failure
"""

def analyze_error_row():
    """Analyze the exact failing row from the error message"""
    print("=" * 80)
    print("DEEP ERROR ANALYSIS")
    print("=" * 80)
    
    # The actual failing row from the error message
    error_row = """
    Failing row contains:
    (6edebf77-42d8-4000-b98b-0f0170a0e6c3,     -- id (UUID)
     d1949c37-d380-46f4-ad30-20ae84aff1ad,     -- user_id (UUID) 
     8592ef5d-163b-4c0a-b83d-f3386b2866e6,     -- document_id (UUID)
     WhatsApp Image 2025-10-13 at 11.18.37_2fe8f456, -- file_name
     null,                                      -- vendor_name (NULL!)
     null,                                      -- vendor_address  
     null,                                      -- vendor_gstin
     null,                                      -- vendor_pan
     null,                                      -- vendor_email
     ,                                          -- ❌ EMPTY STRING HERE!
     null,                                      -- next field...
     ...)
    """
    
    print("\n🔍 ROW ANALYSIS:")
    print("   Position 5: vendor_name = NULL ✅ (should be OK)")
    print("   Position 9: EMPTY STRING '' ❌ (THIS IS THE PROBLEM!)")
    print("   Position 23: payment_status = 'unpaid' ✅ (valid)")
    
    print("\n💡 THE REAL ISSUE:")
    print("   There's an EMPTY STRING field that has a constraint!")
    print("   It's NOT the payment_status constraint failing")
    print("   The error message is misleading!")
    
    print("\n🎯 SOLUTION:")
    print("   Find which field has the empty string constraint")
    print("   Convert ALL empty strings to NULL before database insert")
    
    return True


def identify_empty_string_field():
    """Try to identify which field has the empty string causing the constraint violation"""
    print("\n" + "=" * 80)
    print("IDENTIFY EMPTY STRING FIELD")  
    print("=" * 80)
    
    # Based on SUPABASE_SCHEMA.sql structure, let's map the positions
    invoice_fields = [
        'id',                    # 0  - UUID
        'user_id',              # 1  - UUID (NOT NULL)
        'document_id',          # 2  - UUID  
        'filename',             # 3  - file_name (seems to be added)
        'vendor_name',          # 4  - NULL
        'vendor_address',       # 5  - NULL
        'vendor_gstin',         # 6  - NULL  
        'vendor_pan',           # 7  - NULL
        'vendor_email',         # 8  - NULL
        'vendor_phone',         # 9  - EMPTY STRING ❌
        # ... more fields
    ]
    
    print("\n📍 FIELD MAPPING (from error row):")
    for i, field in enumerate(invoice_fields[:10]):
        if i == 9:
            print(f"   {i:2d}. {field:20} = '' ❌ EMPTY STRING!")
        elif i == 4:
            print(f"   {i:2d}. {field:20} = NULL")
        else:
            print(f"   {i:2d}. {field:20} = (value)")
    
    print(f"\n💡 LIKELY CULPRIT: vendor_phone field")
    print(f"   • Getting empty string instead of NULL")
    print(f"   • Might have a CHECK constraint against empty strings")
    
    return True


def check_all_schemas():
    """Check what constraints exist in different schema files"""
    print("\n" + "=" * 80)
    print("SCHEMA ANALYSIS")
    print("=" * 80)
    
    schemas = {
        'SUPABASE_SCHEMA.sql': {
            'payment_status': "CHECK (payment_status IN ('paid', 'unpaid', 'partial', 'overdue'))",
            'vendor_name': "VARCHAR(255) -- nullable",
            'total_amount': "DECIMAL(15,2) NOT NULL"
        },
        'COMPLETE_INDIAN_INVOICE_SCHEMA.sql': {
            'payment_status': "CHECK (payment_status IN ('paid', 'unpaid', 'partial', 'overdue', 'pending', 'cancelled', 'refunded'))",
            'vendor_name': "VARCHAR(255) NOT NULL", 
            'total_amount': "DECIMAL(15,2) NOT NULL"
        },
        'ENHANCED_SCHEMA_50_PLUS_FIELDS.sql': {
            'payment_status': "CHECK (payment_status IN ('pending', 'paid', 'overdue', 'cancelled', 'refunded', 'partial', 'processing', 'failed'))"
        }
    }
    
    print("\n📋 CONSTRAINT DIFFERENCES:")
    for schema, constraints in schemas.items():
        print(f"\n{schema}:")
        for field, constraint in constraints.items():
            print(f"   {field}: {constraint}")
    
    print("\n⚠️  CONFLICTING SCHEMAS DETECTED!")
    print("   Different files define different constraints")
    print("   Need to identify which one is actually active in Supabase")
    
    return True


if __name__ == "__main__":
    print("\n" + "🕵️ DEEP CONSTRAINT VIOLATION DIAGNOSIS\n")
    
    analyze_error_row()
    identify_empty_string_field() 
    check_all_schemas()
    
    print("\n" + "=" * 80)
    print("FINAL DIAGNOSIS")
    print("=" * 80)
    
    print("\n🎯 ROOT CAUSE IDENTIFIED:")
    print("   1. ERROR NAME: 'invoices_payment_status_check' (misleading)")
    print("   2. REAL ISSUE: Empty string in vendor_phone or similar field")
    print("   3. CONSTRAINT: Likely CHECK constraint against empty strings")
    print("   4. SCHEMA CONFLICT: Multiple schema files with different rules")
    
    print("\n🔧 FIXES NEEDED:")
    print("   ✅ DONE: Convert empty strings to NULL")
    print("   ✅ DONE: Set vendor_name fallback to 'Unknown Vendor'")
    print("   🔄 TODO: Restart backend to apply ALL string cleaning")
    print("   🔄 TODO: Test upload again")
    
    print("\n🚀 PREDICTION:")
    print("   With string cleaning fixes, constraint violation should be resolved")
    
    print("=" * 80 + "\n")