#!/usr/bin/env python3
"""
TEST ENHANCED SCHEMA FIXES: Verify payment_status validation matches ENHANCED_SCHEMA_50_PLUS_FIELDS.sql
"""

def test_payment_status_validation():
    """Test that our payment_status validation matches the actual database constraint"""
    
    print("🧪 TESTING ENHANCED SCHEMA PAYMENT_STATUS VALIDATION...")
    print()
    
    # The ENHANCED_SCHEMA_50_PLUS_FIELDS.sql constraint:
    # CHECK (payment_status IN ('pending', 'paid', 'overdue', 'cancelled', 'refunded', 'partial', 'processing', 'failed'))
    
    # Import our validation function
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
    
    try:
        from app.services.document_processor import DocumentProcessor
        
        processor = DocumentProcessor("")
        
        print("🎯 TESTING VALID VALUES (should return as-is):")
        valid_values = ['pending', 'paid', 'overdue', 'cancelled', 'refunded', 'partial', 'processing', 'failed']
        for value in valid_values:
            result = processor._validate_payment_status(value)
            status = "✅ PASS" if result == value else f"❌ FAIL (got {result})"
            print(f"   {value} → {result} {status}")
        
        print()
        print("🎯 TESTING INVALID VALUES (should map to valid ones):")
        invalid_tests = {
            'unpaid': 'pending',     # Key fix: unpaid → pending
            'unknown': 'pending',
            'draft': 'pending',
            'na': 'pending',
            'n/a': 'pending',
            '': 'pending',           # Empty should default to pending
            None: 'pending',         # None should default to pending
            'invalid_test': 'pending'  # Unknown should default to pending
        }
        
        for input_val, expected in invalid_tests.items():
            result = processor._validate_payment_status(input_val)
            status = "✅ PASS" if result == expected else f"❌ FAIL (got {result})"
            print(f"   {repr(input_val)} → {result} {status}")
        
        print()
        print("🎯 OVERALL RESULT:")
        print("✅ If all tests pass, payment_status validation is correctly fixed!")
        
    except Exception as e:
        print(f"❌ Error testing: {e}")
        print("💡 Make sure the backend is not running when testing imports")

if __name__ == "__main__":
    test_payment_status_validation()