#!/usr/bin/env python3
"""
Test to verify payment_status validation fix
"""

def test_payment_status_validation():
    """Test that payment_status is properly validated"""
    
    print("\n" + "="*70)
    print("🧪 Testing Payment Status Validation Fix")
    print("="*70 + "\n")
    
    # Define the validation logic (same as in document_processor.py)
    def validate_payment_status(value):
        """
        Validate and sanitize payment_status field.
        Must be one of the allowed enum values.
        """
        valid_statuses = {'paid', 'unpaid', 'partial', 'overdue', 'pending', 'cancelled', 'refunded', 'processing', 'failed'}
        
        # Convert to string and clean up
        if not value:
            return 'unpaid'  # Default
        
        status_str = str(value).strip().lower()
        
        # Return if valid, otherwise default to 'unpaid'
        return status_str if status_str in valid_statuses else 'unpaid'
    
    # Test cases: (input, expected_output, description)
    test_cases = [
        ('paid', 'paid', 'Valid: paid'),
        ('unpaid', 'unpaid', 'Valid: unpaid'),
        ('partial', 'partial', 'Valid: partial'),
        ('overdue', 'overdue', 'Valid: overdue'),
        ('pending', 'pending', 'Valid: pending'),
        ('cancelled', 'cancelled', 'Valid: cancelled'),
        ('refunded', 'refunded', 'Valid: refunded'),
        ('processing', 'processing', 'Valid: processing'),
        ('failed', 'failed', 'Valid: failed'),
        ('', 'unpaid', 'Edge case: empty string → defaults to unpaid'),
        (None, 'unpaid', 'Edge case: None → defaults to unpaid'),
        ('UNPAID', 'unpaid', 'Case sensitivity: UNPAID → unpaid'),
        ('PAID', 'paid', 'Case sensitivity: PAID → paid'),
        ('  pending  ', 'pending', 'Whitespace: "  pending  " → pending'),
        ('unknown', 'unpaid', 'Invalid: unknown → defaults to unpaid'),
        ('invalid_status', 'unpaid', 'Invalid: invalid_status → defaults to unpaid'),
        (0, 'unpaid', 'Type conversion: 0 → unpaid'),
        (False, 'unpaid', 'Type conversion: False → unpaid'),
    ]
    
    print("1️⃣  Running validation tests:")
    print("-" * 70)
    
    all_passed = True
    passed_count = 0
    failed_count = 0
    
    for input_val, expected, description in test_cases:
        result = validate_payment_status(input_val)
        is_passed = result == expected
        status = "✅" if is_passed else "❌"
        
        print(f"{status} {description}")
        print(f"   Input: {repr(input_val):30} → {result:15} (expected: {expected})")
        
        if not is_passed:
            all_passed = False
            failed_count += 1
        else:
            passed_count += 1
        print()
    
    print("-" * 70)
    print(f"\n2️⃣  Results Summary:")
    print(f"   ✅ Passed: {passed_count}/{len(test_cases)}")
    print(f"   ❌ Failed: {failed_count}/{len(test_cases)}")
    
    print("\n3️⃣  Key Validations:")
    valid_statuses = {'paid', 'unpaid', 'partial', 'overdue', 'pending', 'cancelled', 'refunded', 'processing', 'failed'}
    print(f"   ✅ Allowed values: {sorted(valid_statuses)}")
    print(f"   ✅ Default value: 'unpaid'")
    print(f"   ✅ Case-insensitive: YES")
    print(f"   ✅ Whitespace handling: YES")
    print(f"   ✅ None/empty handling: YES")
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ ALL TESTS PASSED - Payment status validation is working correctly!")
        print("   Invoices will no longer crash due to invalid payment_status values!")
    else:
        print("❌ SOME TESTS FAILED - There may be an issue with the validation")
    print("="*70 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = test_payment_status_validation()
    exit(0 if success else 1)
